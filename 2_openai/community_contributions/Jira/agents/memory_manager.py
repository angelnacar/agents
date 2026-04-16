import os
import sqlite3
import json
import numpy as np
import sqlite_vss
from typing import List, Dict, Any
from openai import OpenAI



class ChatMemory:
    """
    Sistema de memoria persistente utilizando SQLite y sqlite-vss para 
    almacenar y recuperar preferencias y eventos mediante búsqueda semántica (RAG).
    """
    def __init__(self, db_name="memory.db", openai_api_key=None):
        self.db_name = db_name
        # Cliente OpenAI dedicado para embeddings
        self.embedding_client = OpenAI(api_key=openai_api_key)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            # Cargar la extensión VSS
            conn.enable_load_extension(True)
            try:
                sqlite_vss.load(conn)
            except Exception as e:
                print(f"⚠️ Advertencia: No se pudo cargar la extensión vss0: {e}")
            
            cursor = conn.cursor()
            # Tabla para preferencias (metadatos)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            # Tabla para eventos (texto plano)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Tabla virtual VSS para los embeddings de los eventos
            # Nota: vss0 requiere que la tabla de datos exista primero
            try:
                cursor.execute("CREATE VIRTUAL TABLE IF NOT EXISTS events_vss USING vss0_vss(event_embedding)");
            except Exception as e:
                print(f"⚠️ Error creando tabla VSS: {e}")
                
            conn.commit()

    def _get_embedding(self, text: str) -> List[float]:
        """Genera un embedding para el texto dado usando OpenAI."""
        text = text.replace("\n", " ")
        response = self.embedding_client.embeddings.create(
            input=[text], 
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def add_preference(self, key: str, value: Any):
        val_str = json.dumps(value, ensure_ascii=False)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, val_str))
            conn.commit()

    def get_preferences(self) -> Dict[str, Any]:
        prefs = {}
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM preferences")
            for row in cursor.fetchall():
                try:
                    prefs[row[0]] = json.loads(row[1])
                except:
                    prefs[row[0]] = row[1]
        return prefs

    def add_to_summary(self, event: str):
        # 1. Guardar el texto en la tabla normal
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO events (event) VALUES (?)", (event,))
            event_id = cursor.lastrowid
            
            # 2. Generar embedding y guardarlo en la tabla VSS
            embedding = self._get_embedding(event)
            # sqlite-vss espera el vector como un string de floats separados por comas o blob
            vector_str = ",".join(map(str, embedding))
            cursor.execute("INSERT INTO events_vss(rowid, event_embedding) VALUES (?, ?)", (event_id, vector_str))
            
            # Mantener limpieza de los últimos 100 eventos para evitar crecimiento infinito
            cursor.execute("""
                DELETE FROM events WHERE id NOT IN 
                (SELECT id FROM events ORDER BY id DESC LIMIT 100)
            """)
            # Nota: En una implementación real, también habría que limpiar events_vss
            conn.commit()

    def get_relevant_context(self, query: str, limit=3) -> str:
        """
        Recupera los fragmentos de memoria más relevantes semánticamente 
        basándose en la consulta del usuario.
        """
        query_vector = self._get_embedding(query)
        vector_str = ",".join(map(str, query_vector))
        
        with sqlite3.connect(self.db_name) as conn:
            conn.enable_load_extension(True)
            try:
                sqlite_vss.load(conn)
            except: pass
            
            cursor = conn.cursor()
            # Query de sqlite-vss para encontrar los más cercanos
            # Buscamos en events_vss y hacemos join con events para obtener el texto
            cursor.execute(f"""
                SELECT e.event 
                FROM events e
                JOIN events_vss v ON e.id = v.rowid
                WHERE v.event_embedding MATCH '?'
                ORDER BY distance
                LIMIT ?
            """, (vector_str, limit))
            
            results = [row[0] for row in cursor.fetchall()]
        
        prefs = self.get_preferences()
        
        context = "MEMORIA SEMÁNTICA RECUPERADA:\n"
        if results:
            context += "- Recuerdos relevantes: " + " | ".join(results) + "\n"
        else:
            context += "- No se encontraron recuerdos específicos para esta consulta.\n"
            
        if prefs:
            context += f"- Preferencias: {json.dumps(prefs, ensure_ascii=False)}\n"
            
        return context

    def get_context_string(self, limit=5) -> str:
        """Mantiene compatibilidad con la versión anterior (recuperación lineal)."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT event FROM events ORDER BY id DESC LIMIT ?", (limit,))
            summary = [row[0] for row in cursor.fetchall()]
            summary.reverse()
        
        prefs = self.get_preferences()
        context = "MEMORIA RECIENTE:\n"
        context += f"- Eventos: {', '.join(summary)}\n"
        context += f"- Preferencias: {json.dumps(prefs, ensure_ascii=False)}\n"
        return context
