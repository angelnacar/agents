from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"""Eres un asistente de investigación experto en planificación estratégica.
Dada una consulta de usuario, tu trabajo es analizar el tema y producir un plan de búsquedas web estructurado.

REQUISITOS:
- Genera exactamente {HOW_MANY_SEARCHES} búsquedas web estratégicas
- Cada búsqueda debe cubrir un aspecto diferente del tema
- Prioriza fuentes diversas y perspectivas variadas
- Asegúrate de que las búsquedas sean específicas y relevantes

GUARDARRAILES:
- NO incluyas búsquedas genéricas o vagas
- NO repitas conceptos similares
- NO te desvías del tema principal de la consulta
- VERIFICA que cada búsqueda aporte valor único al informe final"""


class WebSearchItem(BaseModel):
    reason: str = Field(
        description="Tu razonamiento de por qué esta búsqueda es importante y cómo contribuye al informe final."
    )
    query: str = Field(
        description="El término de búsqueda específico y optimizado para motores de búsqueda."
    )


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="Lista ordenada de búsquedas web a realizar para responder comprehensivamente la consulta."
    )


planner_agent = Agent(
    name="Agente de Planificación",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
