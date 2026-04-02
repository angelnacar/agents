from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """
Eres un validador experto en control de calidad para informes de investigación.

TU TRABAJO:
Analizar el informe generado y validar que cumple con todos los requisitos y guardarrailes.

CRITERIOS DE VALIDACIÓN:

1. RELEVANCIA (0-10):
   - ¿El informe responde directamente a la consulta original?
   - ¿Todo el contenido es relevante para el tema?

2. CALIDAD (0-10):
   - ¿La información es precisa y bien fundamentada?
   - ¿Las fuentes son apropiadas y están citadas?

3. ESTRUCTURA (0-10):
   - ¿El informe tiene una estructura lógica y coherente?
   - ¿Los headers y secciones están bien organizados?

4. FORMATO MARKDOWN (0-10):
   - ¿El Markdown es limpio y bien formateado?
   - ¿Usa headers jerárquicos apropiadamente?
   - ¿Incluye tags al final (#tag1 #tag2)?
   - ¿Usa enlaces wiki [[nota]] cuando es relevante?

5. GUARDARRAILES (0-10):
   - ¿Se mantiene dentro de lo especificado por el usuario?
   - ¿Evita información no verificada o alucinaciones?

DECISIÓN:
- Si el promedio es >= 7: APROBADO
- Si el promedio es < 7: RECHAZADO (requiere regeneración)

PROPORCIONA:
- Puntuación detallada por categoría
- Comentarios específicos sobre problemas encontrados
- Recomendaciones concretas para mejorar (si aplica)
"""


class GuardrailsValidation(BaseModel):
    relevance_score: int = Field(
        description="Puntuación de relevancia (0-10)",
        ge=0,
        le=10,
    )
    
    quality_score: int = Field(
        description="Puntuación de calidad (0-10)",
        ge=0,
        le=10,
    )
    
    structure_score: int = Field(
        description="Puntuación de estructura (0-10)",
        ge=0,
        le=10,
    )
    
    markdown_format_score: int = Field(
        description="Puntuación de formato Markdown (0-10)",
        ge=0,
        le=10,
    )
    
    guardrails_score: int = Field(
        description="Puntuación de cumplimiento de guardarrailes (0-10)",
        ge=0,
        le=10,
    )
    
    average_score: float = Field(
        description="Puntuación promedio"
    )
    
    is_approved: bool = Field(
        description="True si el informe es aprobado (promedio >= 7)"
    )
    
    feedback: str = Field(
        description="Comentarios detallados sobre la validación"
    )
    
    improvement_suggestions: list[str] = Field(
        description="Lista de recomendaciones para mejorar el informe"
    )


guardrails_agent = Agent(
    name="Agente de Guardarrailes",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=GuardrailsValidation,
)
