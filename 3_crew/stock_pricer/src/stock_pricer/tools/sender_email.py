from dotenv import load_dotenv
load_dotenv(override=True)  # ← mover aquí, primera línea ejecutable

import resend
import os
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class EmailModelArgs(BaseModel):
    body: str = Field(description="El cuerpo del correo electrónico a enviar en formato HTML")

class SenderEmailTool(BaseTool):
    name: str = "SenderEmailTool"
    description: str = "Útil para enviar el informe final de inversión detallado al cliente vía correo electrónico. El cuerpo del correo debe ser en formato HTML y contener el informe detallado sobre la empresa elegida y las no seleccionadas."

    def _run(self, body: str) -> str:
        """ Envía un correo electrónico con el cuerpo indicado a todos los clientes potenciales de inversión. """
        
        # Configurar la API Key desde las variables de entorno
        resend.api_key = os.environ.get("RESEND_API_KEY")

        try:
            # En Resend, pasamos un diccionario con los parámetros
            r = resend.Emails.send({
                "from": "onboarding@resend.dev", # Nombre <email>
                "to": ["angelnacar9@gmail.com"],               # Admite una lista de correos
                "subject": "Recomendación de inversión en acciones",  # Asunto del correo
                "html": body,                                    # 'text' para texto plano, 'html' para HTML
            })
            
            return f"Email enviado con éxito. ID: {r['id']}"
            
        except Exception as e:
            return f"Error al enviar email: {str(e)}"