from pydantic import BaseModel, Field
from agents import Agent

instructions = """Eres un agente de seguridad y guardarrailes para la gestión de Jira. Tu misión es analizar las intenciones del usuario y las acciones propuestas por el asistente para prevenir errores críticos o acciones no autorizadas.

Criterios de Seguridad:
1. Acciones Destructivas: Cualquier acción que implique borrar, eliminar o sobrescribir datos (ej. borrar un issue, eliminar un comentario, borrar un proyecto) DEBE ser marcada como 'requiere_confirmacion'.
2. Cambios Masivos: Acciones que afecten a múltiples issues simultáneamente deben ser revisadas.
3. Validación de Intención: Asegúrate de que la acción solicitada coincide con la intención del usuario.

Si una acción es segura y no destructiva, marca 'requiere_confirmacion' como False.
Si la acción es potencialmente peligrosa o destructiva, marca 'requiere_confirmacion' como True y proporciona una advertencia clara para el usuario.
"""

class GuardrailValidation(BaseModel):
    is_safe: bool = Field(
        description="Indica si la acción es segura para ejecutar inmediatamente",
    )
    requiere_confirmacion: bool = Field(
        description="Indica si la acción requiere confirmación explícita del usuario antes de proceder",
    )
    advertencia: str = Field(
        description="Mensaje de advertencia o razón por la cual se requiere confirmación. Si es seguro, dejar vacío.",
    )

guardrails_agent = Agent(
    name="Agente de Guardarrailes",
    instructions=instructions,
    model="gemma4:31b-cloud",
    output_type=GuardrailValidation
)