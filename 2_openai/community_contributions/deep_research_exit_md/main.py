# Arquitectura del Sistema Agéntico: Deep Research Obsidian AI
#
# El sistema implementa un flujo de investigación autónoma basado en la siguiente arquitectura:
#
# 1. Interfaz de Usuario (Gradio): Proporciona la entrada de la consulta y muestra el progreso en tiempo real mediante streaming de Markdown.
# 2. ResearchManager (Orquestador): Actúa como el núcleo del sistema, coordinando la descomposición de la consulta original en sub-tareas de investigación.
# 3. Agentes Especializados (implícitos en ResearchManager):
#    - Planificador: Analiza la consulta y define la estrategia de búsqueda.
#    - Investigador: Ejecuta búsquedas, extrae información de fuentes externas y filtra datos relevantes.
#    - Sintetizador/Redactor: Procesa la información recolectada para generar un informe estructurado en formato Markdown compatible con Obsidian.
# 4. Flujo de Ejecución:
#    - Entrada -> Planificación -> Investigación Iterativa -> Síntesis -> Informe Final.
#
import gradio as gr
import asyncio
from dotenv import load_dotenv
import os
from research_manager import ResearchManager

# Cargar variables de entorno desde el archivo .env
load_dotenv()

async def run_research(query):
    """
    Función puente para ejecutar el ResearchManager asíncrono en Gradio.
    """
    manager = ResearchManager()
    full_response = ""
    
    try:
        async for chunk in manager.run(query):
            full_response += chunk + "\n"
            yield full_response
    except Exception as e:
        yield f"❌ **Error durante la ejecución**: {str(e)}"

def create_ui():
    with gr.Blocks(title="Deep Research Obsidian AI", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🔍 Deep Research Obsidian AI")
        gr.Markdown("Sistema de agentes autónomos para investigación profunda y generación de informes en Markdown.")
        
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="Consulta de Investigación", 
                    placeholder="Ej: El impacto de la computación cuántica en la criptografía actual...",
                    lines=3
                )
                run_button = gr.Button("🚀 Iniciar Investigación", variant="primary")
            
            with gr.Column():
                output_display = gr.Markdown(label="Progreso y Resultado")

        # Evento de clic
        run_button.click(
            fn=run_research,
            inputs=[query_input],
            outputs=[output_display]
        )

    return demo

if __name__ == "__main__":
    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

