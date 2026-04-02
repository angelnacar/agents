import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from datetime import datetime
import re

load_dotenv(override=True)


def sanitize_filename(text: str) -> str:
    """Limpia un texto para usarlo como nombre de archivo"""
    # Eliminar caracteres inválidos
    text = re.sub(r'[<>:"/\\|？*]', '', text)
    # Reemplazar espacios con guiones
    text = text.replace(' ', '_')
    # Limitar longitud
    return text[:50]


async def run_research(query: str):
    """Ejecuta la investigación y genera el informe"""
    if not query or not query.strip():
        yield "", "⚠️ Por favor, introduce una consulta válida"
        return
    
    manager = ResearchManager()
    full_report = ""
    progress = ""
    
    try:
        async for chunk in manager.run(query):
            if chunk.startswith("🔍") or chunk.startswith("📋"):
                progress += chunk + "\n"
            elif chunk.startswith("###"):
                progress += "\n" + chunk + "\n"
            elif chunk.startswith("✅") or chunk.startswith("⚠️") or chunk.startswith("🔄"):
                progress += chunk + "\n"
            elif chunk.startswith("#") or chunk.startswith("---"):
                # Esto es el informe final
                full_report = chunk
            else:
                progress += chunk + "\n"
            
            yield progress, full_report
            
    except Exception as e:
        error_msg = f"❌ **Error**: {str(e)}\n\nVerifica tu API key de OpenAI e inténtalo de nuevo."
        yield progress + "\n\n" + error_msg, ""


def create_download_link(report: str, query: str) -> str:
    """Crea un enlace de descarga para el informe"""
    if not report:
        return ""
    
    # Generar nombre de archivo
    timestamp = datetime.now().strftime("%Y-%m-%d")
    safe_title = sanitize_filename(query[:30])
    filename = f"{timestamp}_{safe_title}.md"
    
    # Crear archivo temporal
    import tempfile
    import os
    
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    
    return filepath


def download_report(report: str, query: str):
    """Prepara el archivo para descarga"""
    if not report:
        return None
    
    filepath = create_download_link(report, query)
    return filepath


# Crear la interfaz Gradio
with gr.Blocks(
    theme=gr.themes.Default(primary_hue="sky", secondary_hue="blue"),
    title="🔍 Deep Research para Obsidian"
) as ui:
    
    gr.Markdown("""
    # 🔍 Deep Research para Obsidian
    
    **Investigación profunda con agentes de IA + guardarrailes de calidad**
    
    Este sistema genera informes detallados en formato Markdown optimizados para **Obsidian**.
    Incluye validación automática de calidad, estructura jerárquica, tags y enlaces wiki.
    
    ---
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            query_input = gr.Textbox(
                label="📝 ¿Qué tema quieres investigar?",
                placeholder="Ej: Inteligencia Artificial en medicina, Historia de la computación cuántica, etc.",
                lines=3,
                info="Describe el tema con detalle para obtener mejores resultados"
            )
            
            research_btn = gr.Button(
                "🚀 Iniciar Investigación",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📊 Características
            
            ✅ **5 búsquedas estratégicas** paralelas  
            ✅ **Validación con guardarrailes** de calidad  
            ✅ **Formato Obsidian** con frontmatter YAML  
            ✅ **Tags y enlaces wiki** automáticos  
            ✅ **Fuentes citadas** correctamente  
            ✅ **1000-2000 palabras** de contenido  
            """)
    
    gr.Markdown("---")
    
    # Sección de progreso
    with gr.Accordion("📈 Progreso de la Investigación", open=True):
        progress_output = gr.Markdown(
            label="Progreso",
            show_copy_button=True
        )
    
    # Sección del informe
    with gr.Accordion("📄 Informe para Obsidian", open=False):
        report_output = gr.Markdown(
            label="Vista Previa del Informe",
            show_copy_button=True,
            height=500
        )
        
        # Botón de descarga
        download_btn = gr.Button(
            "📥 Descargar para Obsidian",
            variant="secondary",
            size="lg"
        )
        
        download_file = gr.File(
            label="Archivo Descargable",
            type="filepath",
            visible=True
        )
    
    # Ejemplos
    gr.Markdown("---")
    gr.Markdown("### 💡 Ejemplos de Consultas")
    
    examples = gr.Examples(
        examples=[
            "Impacto de la inteligencia artificial en el diagnóstico médico temprano",
            "Historia y evolución de los lenguajes de programación funcionales",
            "Cambio climático: tecnologías emergentes para captura de carbono",
            "Filosofía estoica: aplicaciones prácticas en la vida moderna",
            "Computación cuántica: estado actual y perspectivas futuras"
        ],
        inputs=query_input,
        label="Haz clic para usar un ejemplo"
    )
    
    # Conectar eventos
    research_btn.click(
        fn=run_research,
        inputs=query_input,
        outputs=[progress_output, report_output]
    )
    
    query_input.submit(
        fn=run_research,
        inputs=query_input,
        outputs=[progress_output, report_output]
    )
    
    download_btn.click(
        fn=download_report,
        inputs=[report_output, query_input],
        outputs=download_file
    )
    
    # Footer
    gr.Markdown("""
    ---
    
    **💡 Consejo**: Una vez descargado el archivo, guárdalo en tu vault de Obsidian.
    El informe incluye frontmatter YAML, tags y formato optimizado para búsqueda y enlace.
    
    _Generado con OpenAI Agents Framework + Guardrails de Calidad_
    """)


if __name__ == "__main__":
    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        share=False
    )
