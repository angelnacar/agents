# Guía para Recibir y Gestionar Respuestas de Correo con Resend

Esta guía te permitirá recibir las respuestas de los correos electrónicos que envía tu agente y procesarlas automáticamente con IA.

## 📋 Requisitos Previos

1. **Tener una cuenta en Resend** (https://resend.com)
2. **Tener un dominio verificado** en Resend
3. **Tener la API key** configurada en tu archivo `.env`

## 🔧 Paso 1: Instalar Dependencias

```bash
# Desde la carpeta del proyecto
uv pip install -r requirements_email.txt
```

## 🔧 Paso 2: Configurar Variables de Entorno

Añade estas líneas a tu archivo `.env`:

```bash
# API Key de Resend (ya deberías tenerla)
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxx

# Email desde el que se enviarán las respuestas (debe ser de tu dominio verificado)
RESEND_FROM_EMAIL=tu_nombre@tudominio.com
```

## 🔧 Paso 3: Configurar Email Routing en Resend

### 3.1 Usar el Dominio pinbraae.resend.app

Resend te proporciona un dominio preconfigurado: `pinbraae.resend.app`

**Dirección para recibir emails:** `<anything>@pinbraae.resend.app`

Ejemplos:
- `leads@pinbraae.resend.app` - Para leads de ventas
- `support@pinbraae.resend.app` - Para soporte
- `info@pinbraae.resend.app` - Para información general

### 3.2 Configurar Email Routing

1. Ve a https://resend.com/domains
2. Selecciona `pinbraae.resend.app`
3. Ve a la pestaña **"Email Routing"**
4. Haz clic en **"Create Route"**
5. Configura la ruta:
   - **Regex:** `.*` (para recibir todos los emails) o específico como `leads@pinbraae.resend.app`
   - **Action:** `Webhook`
   - **Webhook URL:** `http://localhost:8000/webhook` (para desarrollo)
   - **Status:** ✅ Active

### 3.3 Para Producción (ngrok)

Para que Resend pueda enviar webhooks a tu máquina local, necesitas exponer tu servidor:

```bash
# Instalar ngrok si no lo tienes
# En Linux:
sudo snap install ngrok

# O descargar desde: https://ngrok.com/download

# Crear túnel HTTP
ngrok http 8000
```

Ngrok te dará una URL como: `https://abc123.ngrok.io`

Usa esa URL en Resend: `https://abc123.ngrok.io/webhook`

## 🚀 Paso 4: Ejecutar el Servidor Webhook

```bash
# Desde la carpeta 2_openai
uv run email_response_handler.py
```

Verás:
```
🚀 Iniciando servidor webhook de respuestas de correo...
📍 Webhook endpoint: http://localhost:8000/webhook
📊 Ver correos recibidos: http://localhost:8000/emails
```

## 🧪 Paso 5: Probar el Webhook

### Opción A: Enviar un correo de prueba

1. Envía un correo a tu dirección configurada en Resend
2. Responde a uno de los correos que envió tu agente
3. El webhook recibirá la respuesta automáticamente

### Opción B: Simular un webhook con curl

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "type": "email",
    "id": "test_123",
    "from": "cliente@example.com",
    "to": "tu@tudominio.com",
    "subject": "Re: Email de ventas",
    "text": "Hola, estoy interesado en su producto. ¿Podemos agendar una llamada?",
    "timestamp": "2024-01-01T12:00:00.000Z"
  }'
```

## 📊 Paso 6: Ver Correos Recibidos

### Ver todos los correos

```bash
curl http://localhost:8000/emails
```

### Ver un correo específico

```bash
curl http://localhost:8000/emails/test_123
```

### Responder a un correo

```bash
curl -X POST http://localhost:8000/emails/test_123/reply \
  -H "Content-Type: application/json" \
  -d '{
    "reply_body": "Gracias por su interés. Me encantaría agendar una llamada. ¿Qué día le viene bien?"
  }'
```

## 🤖 Cómo Funciona el Agente de Procesamiento

Cuando llega un correo:

1. **Recepción:** El webhook recibe el email de Resend
2. **Análisis:** El agente de IA analiza el contenido
3. **Clasificación:** Determina sentimiento, interés y clasifica el lead
4. **Sugerencia:** Propone una respuesta apropiada
5. **Almacenamiento:** Guarda el email y análisis en memoria

### Ejemplo de Salida del Agente:

```
🤖 Análisis del Agente:
1. Sentimiento: Positivo
2. Nivel de interés: Alto
3. Objeciones o preguntas principales: Pregunta sobre disponibilidad para una llamada
4. Sugerencia de respuesta: Confirmar disponibilidad y proponer horarios específicos
5. Clasificación del lead: Caliente
```

## 📝 Integración con el Agente de Ventas

Para integrar esto con tu agente de ventas actual, modifica el script para que:

1. **Guarde los IDs** de los correos enviados
2. **Relacione las respuestas** con los correos originales
3. **Dispare acciones** basadas en el análisis del agente

### Ejemplo de Integración:

```python
# En tu agente de ventas, guarda el ID del correo enviado
@function_tool
def send_email(body: str, prospect_id: str):
    """Envía email y guarda el ID para tracking"""
    r = resend.Emails.send({...})
    email_id = r["id"]
    
    # Guardar en base de datos
    save_sent_email(prospect_id, email_id)
    
    return {"status": "success", "id": email_id}
```

## 🔒 Consideraciones de Seguridad

### Validar Webhooks de Resend

En producción, deberías validar que los webhooks vienen realmente de Resend:

```python
from fastapi import Request, HTTPException
import hmac
import hashlib

@app.post("/webhook")
async def handle_email_webhook(request: Request):
    # Obtener firma del header
    signature = request.headers.get("X-Resend-Signature")
    
    # Verificar firma (implementar validación)
    if not verify_resend_signature(signature, body):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Continuar con el procesamiento...
```

## 🗄️ Persistencia de Datos

Actualmente, los correos se guardan en memoria. Para producción:

1. **Usa una base de datos** (PostgreSQL, MongoDB, etc.)
2. **Implementa colas de mensajes** (Redis, RabbitMQ)
3. **Considera usar un servicio** como Supabase o Firebase

## 🎯 Siguientes Pasos

1. **Añadir base de datos** para persistir correos
2. **Implementar autenticación** en los endpoints
3. **Crear dashboard** para visualizar respuestas
4. **Configurar notificaciones** en tiempo real
5. **Integrar con CRM** para seguimiento de leads

## 📚 Recursos Adicionales

- Documentación de Resend: https://resend.com/docs
- Email Routing: https://resend.com/docs/send-email-routing
- Webhooks: https://resend.com/docs/send-webhooks
- FastAPI: https://fastapi.tiangolo.com/

## 🆘 Solución de Problemas

### El webhook no recibe correos

1. Verifica que el dominio esté verificado en Resend
2. Comprueba que los registros DNS estén propagados
3. Asegúrate de que ngrok esté corriendo (si estás en local)
4. Revisa los logs del servidor

### Error de SSL

```bash
uv pip install --upgrade certifi
```

### Correos van a spam

1. Verifica que SPF, DKIM y DMARC estén configurados
2. Usa un dominio con buena reputación
3. Evita contenido sospechoso en los emails

---

¡Listo! Ahora tu agente puede **recibir y procesar respuestas** automáticamente. 🎉
