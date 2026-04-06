from agents import Agent, WebSearchTool, function_tool
from pydantic import BaseModel, Field
from agents import Runner

INSTRUCTIONS = """
Eres un asistente de investigación especializado en búsqueda y síntesis de información web.

TU TRABAJO:
1. Buscar en la web usando el término proporcionado
2. Analizar múltiples fuentes (mínimo 3-5 fuentes relevantes)
3. Sintetizar la información en un resumen conciso y objetivo

FORMATO DE SALIDA:
- Resumen de 2-3 párrafos
- Máximo 300 palabras
- Captura los puntos clave y datos importantes
- Menciona las fuentes principales (nombres de sitios/web)
- Mantén un tono objetivo y neutral

GUARDARRAILES:
- NO incluyas opiniones personales
- NO especules sobre información no verificada
- NO uses fuentes de baja calidad (blogs personales sin referencias, etc.)
- PRIORIZA fuentes académicas, noticias reconocidas, papers, documentación oficial
- Si la información es contradictoria, menciónalo explícitamente

IMPORTANTE:
Este resumen será usado por un escritor para crear un informe detallado.
Sé preciso, conciso y captura la esencia sin fluff."""

# Agente interno que ejecuta la búsqueda (usado por la tool)
_search_executor_agent = Agent(
    name="Ejecutor de Búsqueda",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o-mini",
)

@function_tool
async def execute_web_search(query: str, reason: str = "") -> str:
    """
    Ejecuta una búsqueda web y retorna un resumen sintetizado de los resultados.
    
    Args:
        query: El término de búsqueda específico
        reason: Opcional. El razonamiento de por qué esta búsqueda es importante
        
    Returns:
        Un resumen de 2-3 párrafos con los puntos clave encontrados
    """
    input_text = f"Término de búsqueda: {query}"
    if reason:
        input_text += f"\nRazón: {reason}"
    
    try:
        result = await Runner.run(_search_executor_agent, input_text)
        return str(result.final_output)
    except Exception as e:
        return f"Error técnico durante la búsqueda web: {type(e).__name__} - {str(e)}"
