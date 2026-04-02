from agents import Runner, trace, gen_trace_id
from typing import AsyncGenerator
import asyncio

from agents.planner_agent import planner_agent, WebSearchPlan
from agents.search_agent import search_agent
from agents.writer_agent import writer_agent, ReportData
from agents.guardrails_agent import guardrails_agent, GuardrailsValidation


class ResearchManager:
    """
    Gestor de investigación profunda con guardarrailes y salida para Obsidian.
    
    Flujo:
    1. Planifica búsquedas
    2. Ejecuta búsquedas en paralelo
    3. Genera informe
    4. Valida con guardarrailes
    5. Regenera si es necesario
    6. Retorna informe final
    """

    MAX_REGENERATIONS = 2  # Máximo de intentos si falla validación
    MIN_APPROVAL_SCORE = 7.0  # Puntuación mínima para aprobar

    async def run(self, query: str) -> AsyncGenerator[str, None]:
        """
        Ejecuta el proceso completo de investigación profunda.
        
        Args:
            query: La consulta de investigación del usuario
            
        Yields:
            Mensajes de progreso y el informe final
        """
        trace_id = gen_trace_id()
        with trace("Investigación Obsidian", trace_id=trace_id):
            yield f"🔍 **Trazabilidad**: [Ver trace](https://platform.openai.com/traces/trace?trace_id={trace_id})\n"
            yield f"📋 **Consulta**: {query}\n\n---\n"
            
            # Fase 1: Planificación
            yield "### 📍 Fase 1: Planificando investigación..."
            search_plan = await self._plan_searches(query)
            yield f"✅ **Plan generado**: {len(search_plan.searches)} búsquedas estratégicas\n\n"
            
            # Fase 2: Búsqueda
            yield "### 🔎 Fase 2: Ejecutando búsquedas..."
            search_results = await self._perform_searches(search_plan)
            yield f"✅ **Búsquedas completadas**: {len(search_results)} resultados obtenidos\n\n"
            
            # Fase 3: Escritura del informe
            yield "### ✍️ Fase 3: Generando informe..."
            report = await self._write_report(query, search_results)
            yield f"✅ **Informe generado**: {len(report.markdown_report)} caracteres\n\n"
            
            # Fase 4: Validación con guardarrailes
            yield "### 🛡️ Fase 4: Validando calidad..."
            validation = await self._validate_report(query, report)
            
            if validation.is_approved:
                yield f"✅ **Validación APROBADA** (Score: {validation.average_score:.1f}/10)\n\n"
            else:
                yield f"⚠️ **Validación RECHAZADA** (Score: {validation.average_score:.1f}/10)\n"
                yield f"📝 **Feedback**: {validation.feedback}\n\n"
                
                # Intentar regenerar
                report = await self._regenerate_report(
                    query, search_results, report, validation
                )
                validation = await self._validate_report(query, report)
                
                if validation.is_approved:
                    yield f"✅ **Re-validación APROBADA** (Score: {validation.average_score:.1f}/10)\n\n"
                else:
                    yield f"⚠️ **Advertencia**: El informe no alcanza la puntuación óptima, pero se entrega para revisión manual.\n\n"
            
            # Resumen final
            yield "### 📊 Resumen de la Investigación\n\n"
            yield f"**Título**: {report.title}\n\n"
            yield f"**Resumen**: {report.short_summary}\n\n"
            yield f"**Tags**: {', '.join(report.tags)}\n\n"
            yield f"**Fuentes**: {len(report.sources)} fuentes consultadas\n\n"
            yield f"**Preguntas para continuar**: {len(report.follow_up_questions)}\n\n"
            
            yield "---\n\n"
            yield "### 📥 **Informe Completo para Obsidian**\n\n"
            yield "El informe está listo para descargar. Usa el botón de descarga para guardarlo en tu vault de Obsidian.\n\n"
            
            # Retornar el informe completo (para la descarga)
            yield report.markdown_report

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        """Planifica las búsquedas a realizar"""
        result = await Runner.run(
            planner_agent,
            f"Consulta: {query}",
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Ejecuta las búsquedas en paralelo"""
        tasks = [
            asyncio.create_task(self._search(item))
            for item in search_plan.searches
        ]
        
        results = []
        for completed in asyncio.as_completed(tasks):
            result = await completed
            if result is not None:
                results.append(result)
        
        return results

    async def _search(self, item) -> str | None:
        """Ejecuta una búsqueda individual"""
        input_text = f"Término de búsqueda: {item.query}\nRazón: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return None

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Genera el informe"""
        input_text = (
            f"Consulta original: {query}\n\n"
            f"Resultados de búsqueda:\n{chr(10).join(search_results)}"
        )
        
        result = await Runner.run(writer_agent, input_text)
        return result.final_output_as(ReportData)

    async def _validate_report(
        self, query: str, report: ReportData
    ) -> GuardrailsValidation:
        """Valida el informe con guardarrailes"""
        input_text = (
            f"Consulta original: {query}\n\n"
            f"Informe generado:\n{report.markdown_report}"
        )
        
        result = await Runner.run(guardrails_agent, input_text)
        return result.final_output_as(GuardrailsValidation)

    async def _regenerate_report(
        self,
        query: str,
        search_results: list[str],
        previous_report: ReportData,
        validation: GuardrailsValidation,
    ) -> ReportData:
        """Regenera el informe con feedback del validador"""
        yield "🔄 Regenerando informe con feedback...\n"
        
        input_text = (
            f"Consulta original: {query}\n\n"
            f"Resultados de búsqueda:\n{chr(10).join(search_results)}\n\n"
            f"Informe anterior:\n{previous_report.markdown_report}\n\n"
            f"Feedback del validador:\n{validation.feedback}\n\n"
            f"Sugerencias de mejora:\n{chr(10).join(validation.improvement_suggestions)}\n\n"
            f"INSTRUCCIÓN: Regenera el informe mejorando los puntos señalados. "
            f"Mantén el formato Obsidian y asegúrate de cumplir todos los guardarrailes."
        )
        
        result = await Runner.run(writer_agent, input_text)
        return result.final_output_as(ReportData)
