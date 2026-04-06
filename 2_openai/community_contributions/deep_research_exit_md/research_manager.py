from agents import Runner, trace, gen_trace_id
from typing import AsyncGenerator
from agentes.lead_agent import lead_agent
from agentes.writer_agent import ReportData

class ResearchManager:
    """
    Gestor de investigación profunda optimizado según buenas praxis de OpenAI Agents.
    
    Sustituye la orquestación manual de Python por un flujo agéntico:
    Lead Agent (Búsqueda Iterativa) -> Writer Agent (Sintetización) -> Guardrail (Calidad)
    """

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        trace_id = gen_trace_id()
        with trace("Investigación Obsidian Optimizada", trace_id=trace_id):
            yield f"🔍 **Trazabilidad**: [Ver trace](https://platform.openai.com/traces/trace?trace_id={trace_id})\n"
            yield f"📋 **Consulta**: {query}\n\n---\n"
            
            yield "🚀 **Iniciando proceso agéntico de investigación...**\n"
            yield "El Lead Agent está razonando, buscando y validando la información...\n\n"
            
            try:
                # El Runner maneja todo el ciclo de vida: 
                # 1. Lead Agent decide qué buscar (Tool calls)
                # 2. Lead Agent decide cuándo ha terminado y hace handoff al Writer
                # 3. Writer genera el ReportData
                # 4. El Guardrail valida el ReportData (si falla, el SDK regenera automáticamente)
                result = await Runner.run(lead_agent, query)
                
                # Intentamos obtener la salida estructurada
                report = result.final_output_as(ReportData)
                
                # Validación de seguridad: si el resultado es un string, el agente no respetó el output_type
                if isinstance(report, str):
                    yield "⚠️ **Aviso**: El agente devolvió un texto plano en lugar de un informe estructurado. Intentando recuperar contenido...\n"
                    # Creamos un ReportData mínimo para evitar que la app rompa
                    report = ReportData(
                        title="Informe de Investigación",
                        short_summary="Resumen no disponible (salida no estructurada)",
                        markdown_report=report,
                        sources=[],
                        tags=[],
                        follow_up_questions=[]
                    )
                
                yield "✅ **Investigación completada y validada por guardrails.**\n\n"

                
                # Resumen final
                yield "### 📊 Resumen de la Investigación\n\n"
                yield f"**Título**: {report.title}\n\n"
                yield f"**Resumen**: {report.short_summary}\n\n"
                yield f"**Tags**: {', '.join(report.tags)}\n\n"
                yield f"**Fuentes**: {len(report.sources)} fuentes consultadas\n\n"
                yield f"**Preguntas para continuar**: {len(report.follow_up_questions)}\n\n"
                
                yield "---\n\n"
                yield "### 📥 **Informe Completo para Obsidian**\n\n"
                yield report.markdown_report
                
            except Exception as e:
                yield f"❌ **Error crítico en el flujo agéntico**: {str(e)}"
