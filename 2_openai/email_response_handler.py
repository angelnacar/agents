"""
Servidor webhook para recibir respuestas de correos electrónicos desde Resend
y procesarlas con agentes de IA.

Configuración necesaria en Resend:
1. Ve a https://resend.com/domains
2. Usa tu dominio: pinbraae.resend.app
3. Configura Email Routing:
   - Regex: .* (para todos los emails)
   - Webhook: http://localhost:8000/webhook (o tu URL de ngrok)
4. Asegúrate de tener RESEND_API_KEY en tu archivo .env

Dirección para recibir emails: <anything>@pinbraae.resend.app
Ejemplo: leads@pinbraae.resend.app, support@pinbraae.resend.app, etc.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
import resend
from agents import Agent, Runner
import asyncio
import json

# Cargar variables de entorno
load_dotenv(override=True)

# Configurar API key de Resend
resend.api_key = os.environ.get("RESEND_API_KEY")

# Crear aplicación FastAPI
app = FastAPI(title="Email Response Handler")

# Agente para procesar respuestas de correo
email_response_agent = Agent(
    name="Email Response Processor",
    instructions="""Eres un agente especializado en procesar respuestas de correos electrónicos de ventas.
    Tu tarea es:
    1. Analizar el contenido del correo recibido
    2. Determinar si es una respuesta positiva, negativa o neutral
    3. Extraer información importante (interés, objeciones, preguntas)
    4. Sugerir una respuesta apropiada
    5. Clasificar el lead (caliente, tibio, frío)
    
    Responde de forma estructurada y concisa.""",
    model="gpt-4o-mini"
)

# Almacenamiento temporal de respuestas (en producción usarías una base de datos)
received_emails = []


@app.post("/webhook")
async def handle_email_webhook(request: Request):
    """
    Endpoint que recibe las respuestas de correo desde Resend.
    
    Resend enviará un POST con el siguiente formato:
    {
        "id": "email_id",
        "from": "replier@example.com",
        "to": "tu@tudominio.com",
        "subject": "Re: Email de ventas",
        "text": "Contenido del correo en texto plano",
        "html": "<p>Contenido en HTML</p>",
        "timestamp": "2024-01-01T00:00:00.000Z"
    }
    """
    try:
        # Obtener los datos del webhook
        data = await request.json()
        
        # Validar que es un evento de email (Resend envía un tipo de evento)
        event_type = data.get("type", "email")
        
        if event_type == "email":
            # Extraer información del correo
            email_data = {
                "id": data.get("id"),
                "from": data.get("from"),
                "to": data.get("to"),
                "subject": data.get("subject"),
                "text": data.get("text", ""),
                "html": data.get("html", ""),
                "timestamp": data.get("timestamp")
            }
            
            # Guardar el correo recibido
            received_emails.append(email_data)
            
            # Procesar con el agente de IA
            print(f"\n📧 Nuevo correo recibido de: {email_data['from']}")
            print(f"Asunto: {email_data['subject']}")
            print("-" * 50)
            
            # Crear prompt para el agente
            prompt = f"""
Analiza esta respuesta de correo electrónico:

De: {email_data['from']}
Para: {email_data['to']}
Asunto: {email_data['subject']}

Contenido:
{email_data['text']}

Proporciona:
1. Sentimiento (positivo/negativo/neutral)
2. Nivel de interés (alto/medio/bajo)
3. Objeciones o preguntas principales
4. Sugerencia de respuesta
5. Clasificación del lead (caliente/tibio/frío)
"""
            
            # Ejecutar el agente
            result = await Runner.run(email_response_agent, prompt)
            
            print("\n🤖 Análisis del Agente:")
            print(result.final_output)
            print("=" * 50)
            
            # Guardar el análisis junto con el correo
            email_data["analysis"] = result.final_output
            email_data["processed"] = True
            
            return JSONResponse(
                status_code=200,
                content={"status": "success", "message": "Email processed"}
            )
        else:
            raise HTTPException(status_code=400, detail=f"Event type {event_type} not supported")
            
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/emails")
async def get_received_emails():
    """Obtener todos los correos recibidos y procesados"""
    return {"emails": received_emails}


@app.get("/emails/{email_id}")
async def get_email_by_id(email_id: str):
    """Obtener un correo específico por ID"""
    for email in received_emails:
        if email.get("id") == email_id:
            return email
    raise HTTPException(status_code=404, detail="Email not found")


@app.post("/emails/{email_id}/reply")
async def reply_to_email(email_id: str, reply_body: str):
    """
    Responder a un correo recibido usando Resend.
    
    Args:
        email_id: ID del correo original
        reply_body: Contenido de la respuesta
    """
    # Buscar el correo original
    original_email = None
    for email in received_emails:
        if email.get("id") == email_id:
            original_email = email
            break
    
    if not original_email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    try:
        # Enviar respuesta con Resend
        response = resend.Emails.send({
            "from": os.environ.get("RESEND_FROM_EMAIL", "onboarding@resend.dev"),
            "to": [original_email["from"]],
            "subject": f"Re: {original_email['subject']}",
            "text": reply_body,
            "in_reply_to": original_email["id"]  # Referencia al correo original
        })
        
        return {
            "status": "success",
            "message": "Reply sent",
            "reply_id": response.get("id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send reply: {str(e)}")


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud"""
    return {"status": "healthy", "emails_received": len(received_emails)}


if __name__ == "__main__":
    print("🚀 Iniciando servidor webhook de respuestas de correo...")
    print("📍 Webhook endpoint: http://localhost:8000/webhook")
    print("📊 Ver correos recibidos: http://localhost:8000/emails")
    print("=" * 50)
    
    # Iniciar servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)
