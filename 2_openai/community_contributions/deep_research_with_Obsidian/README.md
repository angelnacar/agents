# 🔍 Deep Research para Obsidian

Sistema de **investigación profunda con agentes de IA** que genera informes detallados en formato Markdown optimizados para **Obsidian**.

## ✨ Características

- 🤖 **Multi-Agente**: 4 agentes especializados (Planificador, Búsqueda, Escritura, Validación)
- 🛡️ **Guardarrailes de Calidad**: Validación automática con scoring y regeneración
- 📝 **Formato Markdown Limpio**: Tags, enlaces wiki, sin frontmatter YAML
- 📥 **Descarga Directa**: Botón para descargar el informe listo para guardar
- 🔍 **Búsquedas Paralelas**: 5 búsquedas web estratégicas ejecutadas concurrentemente
- 📊 **Trazabilidad**: OpenAI Traces para monitoreo del proceso

## 🏗️ Arquitectura

```
┌─────────────────────────┐
│     ResearchManager     │
└──────────┬──────────────┘
           │
    ┌──────▼──────┐
    │  Guardrails │ ← Validación de calidad
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Planner    │ ← Planifica 5 búsquedas
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Search    │ ← Búsquedas web paralelas
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Writer    │ ← Genera informe Markdown
    └─────────────┘
```

## 🚀 Instalación

### Opción 1: Con `uv` (recomendado)

```bash
cd deep_research_with_Obsidian
uv sync
uv run python main.py
```

### Opción 2: Con `pip`

```bash
cd deep_research_with_Obsidian
pip install -r requirements.txt
python main.py
```

## ⚙️ Configuración

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` y añade tu API key:
```env
OPENAI_API_KEY=sk-...
```

## 💡 Uso

1. **Inicia la aplicación**:
   ```bash
   uv run python main.py
   ```

2. **Abre el navegador** en `http://localhost:7860`

3. **Introduce tu consulta** en el campo de texto

4. **Haz clic en "🚀 Iniciar Investigación"**

5. **Espera el proceso**:
   - 📍 Planificación de búsquedas
   - 🔎 Ejecución de búsquedas paralelas
   - ✍️ Generación del informe
   - 🛡️ Validación con guardarrailes

6. **Descarga el informe** con el botón "📥 Descargar para Obsidian"

7. **Guarda en tu vault** de Obsidian

## 📄 Formato del Informe

El informe generado incluye:

```markdown
# Título del Informe

## Resumen Ejecutivo
...

## Contenido Principal
...

## Enlaces Relacionados
[[Nota relacionada]]

## Fuentes
- [Fuente 1](url)
- [Fuente 2](url)

---

#tags #investigación #IA

_Generado por Deep Research Agent_
```

## 🛡️ Sistema de Guardarrailes

El agente de validación evalúa 5 criterios:

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Relevancia** | 20% | ¿Responde a la consulta? |
| **Calidad** | 20% | ¿Información precisa y verificada? |
| **Estructura** | 20% | ¿Organización lógica y coherente? |
| **Formato Markdown** | 20% | ¿Markdown limpio, tags, enlaces wiki? |
| **Guardarrailes** | 20% | ¿Sin alucinaciones, ético, seguro? |

- **Score ≥ 7.0**: Informe aprobado ✅
- **Score < 7.0**: Regeneración automática ⚠️

## 📊 Ejemplos de Consultas

- "Impacto de la inteligencia artificial en el diagnóstico médico"
- "Historia de los lenguajes de programación funcionales"
- "Tecnologías emergentes para captura de carbono"
- "Filosofía estoica aplicada a la vida moderna"
- "Computación cuántica: estado actual y futuro"

## 🔧 Personalización

### Modificar número de búsquedas

Edita `agents/planner_agent.py`:
```python
HOW_MANY_SEARCHES = 5  # Cambia este valor
```

### Ajustar score mínimo de aprobación

Edita `research_manager.py`:
```python
MIN_APPROVAL_SCORE = 7.0  # Cambia este valor
```

### Personalizar instrucciones de agentes

Cada agente tiene su propio archivo en `agents/` con sus instrucciones específicas.

## 📦 Estructura del Proyecto

```
deep_research_with_Obsidian/
├── __init__.py
├── main.py                    # UI Gradio
├── research_manager.py        # Orquestador
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py       # Planificación
│   ├── search_agent.py        # Búsquedas
│   ├── writer_agent.py        # Escritura
│   └── guardrails_agent.py    # Validación
├── prompts/
│   └── guardrails.md          # Instrucciones validación
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Despliegue en Hugging Face Spaces

1. Crea un nuevo Space en HF
2. Sube los archivos del proyecto
3. Configura las variables de entorno:
   - `OPENAI_API_KEY`
4. Elige **Docker** como SDK
5. ¡Listo!

## 📝 Notas

- El informe se descarga como archivo `.md` temporal
- Compatible con cualquier vault de Obsidian
- No requiere configuración de rutas locales
- Funciona en HF Spaces, local, o cualquier entorno

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Algunas ideas:
- Plantillas personalizables
- Exportación directa a Notion
- Integración con Zotero para citas
- Soporte para múltiples idiomas

## 📄 Licencia

MIT License

---

_Hecho con ❤️ usando OpenAI Agents Framework_
