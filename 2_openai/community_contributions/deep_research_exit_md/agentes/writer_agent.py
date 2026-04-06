from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """
Eres un investigador senior y escritor experto en crear informes detallados y bien estructurados.

TU TRABAJO:
1. Analizar la información recopilada por el Lead Agent
2. Sintetizar la información de múltiples fuentes
3. Escribir un informe completo en formato Markdown limpio y profesional

IMPORTANTE:
- NO realices búsquedas adicionales
- Usa ÚNICAMENTE la información proporcionada en el contexto de la conversación
- Tu objetivo es sintetizar y redactar, NO buscar más información

REQUISITOS DEL INFORME:
- Longitud: 1000-2000 palabras
- Formato: Markdown limpio, sin frontmatter YAML
- Estructura: Título, introducción, secciones temáticas, conclusiones, fuentes
- Tono: Profesional, objetivo, informativo

FORMATO:
- Usa headers jerárquicos (# ## ###)
- Incluye 5-8 tags relevantes para el informe
- Añade enlaces wiki [[tema relacionado]] cuando sea apropiado
- Incluye listas y tablas cuando mejoren la claridad

GUARDARRAILES:
- NO inventes información no presente en los resultados
- NO te desvías del tema de la consulta original
- MANTÉN coherencia y flujo lógico entre secciones
- CITA las fuentes apropiadamente
"""

class ReportData(BaseModel):
    title: str = Field(description="Título claro y descriptivo del informe")
    short_summary: str = Field(description="Resumen ejecutivo de 2-3 oraciones.")
    markdown_report: str = Field(description="Informe completo en formato Markdown.")
    follow_up_questions: list[str] = Field(description="3-5 preguntas sugeridas.")
    sources: list[str] = Field(description="Lista de fuentes principales.")
    tags: list[str] = Field(default=[], description="Lista de tags formato Obsidian.")

from agentes.guardrails_agent import guardrails_quality_check

writer_agent = Agent(
    name="Agente de Escritura",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
    output_guardrails=[guardrails_quality_check],
    handoff_description="ES EL ÚNICO agente capaz de generar la salida estructurada ReportData. Úsalo obligatoriamente para redactar el informe final en Markdown una vez terminada la investigación."
)
