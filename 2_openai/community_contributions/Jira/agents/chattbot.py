import os

from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio
import json
from typing import List, Dict, Any

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from guardrails_agent import guardrails_agent
from memory_manager import ChatMemory

# --- CONFIGURACIÓN ---
# Configura tus claves de API y credenciales de Jira
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JIRA_URL = "https://giss.atlassian.net"

# Configuración del servidor MCP de Atlassian (Jira)
server_params = StdioServerParameters(
    command="uvx",
    args=["mcp-atlassian"],
    env={
        "JIRA_URL": JIRA_URL,
        "JIRA_USERNAME": os.getenv("JIRA_USERNAME"),
        "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
        "PATH": os.getenv("PATH", "")
    }
)

client = OpenAI(
    base_url= "http://192.168.3.241:11434/v1",
    api_key="ollama"
)

async def get_mcp_tools(session: ClientSession) -> List[Dict[str, Any]]:
    """Obtiene las herramientas del servidor MCP y las convierte al formato de OpenAI."""
    tools_result = await session.list_tools()
    openai_tools = []
    
    for tool in tools_result.tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema # MCP usa JSON Schema, que es compatible con OpenAI
            }
        })
    return openai_tools

async def run_mcp_tool(session: ClientSession, tool_name: str, arguments: Dict[str, Any]):
    """Ejecuta una herramienta en el servidor MCP."""
    result = await session.call_tool(tool_name, arguments)
    return result.content

async def chat_with_jira():
    """Lógica principal del chatbot que conecta OpenAI con el servidor MCP de Jira."""
    print("🚀 Iniciando Chatbot con conexión a Jira MCP...")
    
    # Inicializar memoria con API Key de OpenAI para embeddings
    memory = ChatMemory(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la sesión MCP
            await session.initialize()
            
            # 1. Obtener herramientas disponibles en el servidor de Jira
            mcp_tools = await get_mcp_tools(session)
            
            # Construir el system prompt inicial
            system_prompt = "Eres un asistente experto en gestión de proyectos. Tienes acceso a Jira a través de herramientas MCP para consultar y gestionar issues.\n\n"
            
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            print("✅ Conectado al servidor MCP. Escribe 'salir' para terminar.")
            
            while True:
                user_input = input("\n👤 Usuario: ")
                if user_input.lower() in ["salir", "exit", "quit"]:
                    break
                
                # --- RAG: Recuperación de Memoria Semántica ---
                # Recuperamos los recuerdos más relevantes para la consulta actual
                relevant_context = memory.get_relevant_context(user_input)
                
                # Creamos una copia de los mensajes para esta iteración inyectando el contexto
                # Solo en el system prompt para no ensuciar el historial de chat
                current_messages = [
                    {"role": "system", "content": system_prompt + relevant_context},
                    *messages
                ]
                
                current_messages.append({"role": "user", "content": user_input})
                
                # 2. Llamada a OpenAI con las herramientas de Jira
                response = client.chat.completions.create(
                    model="gemma4:31b-cloud", # O el modelo que prefieras
                    messages=current_messages,
                    tools=mcp_tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                
                # 3. Manejar la ejecución de herramientas (Tool Calls)
                if response_message.tool_calls:
                    # Añadimos la respuesta del modelo al historial real
                    messages.append(response_message)
                    
                    for tool_call in response_message.tool_calls:
                        tool_name = tool_call.function.name
                        tool_args = json.loads(tool_call.function.arguments)
                        
                        # --- GUARDRAILS CHECK ---
                        # Validamos la acción con el agente de guardarrailes
                        guardrail_prompt = f"Usuario quiere: {user_input}\nAcción propuesta: {tool_name} con argumentos {tool_args}"
                        
                        validation_response = client.chat.completions.create(
                            model="gemma4:31b-cloud",
                            messages=[
                                {"role": "system", "content": guardrails_agent.instructions},
                                {"role": "user", "content": guardrail_prompt}
                            ],
                            response_format={"type": "json_object"}
                        )
                        
                        validation = json.loads(validation_response.choices[0].message.content)
                        
                        if validation.get("requiere_confirmacion"):
                            print(f"\n⚠️  ADVERTENCIA DE SEGURIDAD: {validation.get('advertencia')}")
                            confirm = input("¿Deseas proceder con esta acción? (si/no): ")
                            if confirm.lower() not in ["si", "yes", "s"]:
                                print("❌ Acción cancelada por el usuario.")
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": "Acción cancelada por el usuario debido a que requería confirmación de seguridad."
                                })
                                continue

                        print(f"🛠️ Ejecutando herramienta de Jira: {tool_name}...")
                        tool_result = await run_mcp_tool(session, tool_name, tool_args)
                        
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(tool_result)
                        })
                    
                    # Obtener la respuesta final del modelo tras ejecutar las herramientas
                    # Usamos de nuevo el contexto RAG para la respuesta final
                    final_messages = [
                        {"role": "system", "content": system_prompt + relevant_context},
                        *messages
                    ]
                    final_response = client.chat.completions.create(
                        model="gemma4:31b-cloud",
                        messages=final_messages
                    )
                    final_text = final_response.choices[0].message.content
                    
                    # --- APRENDIZAJE ---
                    # Pedimos al modelo que extraiga cualquier preferencia o dato relevante para recordar
                    learning_prompt = f"Analiza la siguiente interacción y extrae preferencias del usuario o hechos clave que debamos recordar para el futuro. Responde solo en JSON con el formato: {{\"preference\": \"clave\", \"value\": \"valor\", \"event\": \"resumen corto del evento\"}} o null si no hay nada relevante.\n\nUsuario: {user_input}\nBot: {final_text}"
                    
                    learning_res = client.chat.completions.create(
                        model="gemma4:31b-cloud",
                        messages=[{"role": "user", "content": learning_prompt}],
                        response_format={"type": "json_object"}
                    )
                    
                    try:
                        learning_data = json.loads(learning_res.choices[0].message.content)
                        if learning_data:
                            if "preference" in learning_data:
                                memory.add_preference(learning_data["preference"], learning_data["value"])
                            if "event" in learning_data:
                                memory.add_to_summary(learning_data["event"])
                    except:
                        pass

                    print(f"\n🤖 Bot: {final_text}")
                    messages.append({"role": "assistant", "content": final_text})
                else:
                    # Respuesta directa sin herramientas
                    final_text = response_message.content
                    print(f"\n🤖 Bot: display(Markdown({final_text}))")
                    messages.append({"role": "assistant", "content": final_text})
                    
                    # También aprendemos de respuestas directas
                    learning_prompt = f"Analiza la siguiente interacción y extrae preferencias del usuario o hechos clave que debamos recordar para el futuro. Responde solo en JSON con el formato: {{\"preference\": \"clave\", \"value\": \"valor\", \"event\": \"resumen corto del evento\"}} o null si no hay nada relevante.\n\nUsuario: {user_input}\nBot: {final_text}"
                    learning_res = client.chat.completions.create(
                        model="gemma4:31b-cloud",
                        messages=[{"role": "user", "content": learning_prompt}],
                        response_format={"type": "json_object"}
                    )
                    try:
                        learning_data = json.loads(learning_res.choices[0].message.content)
                        if learning_data:
                            if "preference" in learning_data:
                                memory.add_preference(learning_data["preference"], learning_data["value"])
                            if "event" in learning_data:
                                memory.add_to_summary(learning_data["event"])
                    except:
                        pass

if __name__ == "__main__":
    try:
        asyncio.run(chat_with_jira())
    except KeyboardInterrupt:
        print("\n👋 Chatbot cerrado.")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
