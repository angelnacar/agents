"""
Gestor de Gastos Personales - Punto de Entrada

Este módulo es el punto de entrada principal de la aplicación.
Configura y lanza la interfaz de Gradio con todas las funcionalidades:
- Autenticación (login/registro)
- Registro de gastos
- Categorización automática
- Visualización de estadísticas
"""

import gradio as gr
import matplotlib.pyplot as plt
from datetime import datetime

from repositories import UserRepository, ExpenseRepository, CategoryRepository
from services import AuthService, ExpenseService, CategorizationService, StatisticsService
from utils.constants import MONTH_NAMES


def create_services():
    """Crea e inicializa todos los servicios de la aplicación."""
    user_repository = UserRepository()
    expense_repository = ExpenseRepository()
    category_repository = CategoryRepository()
    
    categorization_service = CategorizationService(category_repository)
    auth_service = AuthService(user_repository)
    expense_service = ExpenseService(expense_repository, categorization_service)
    statistics_service = StatisticsService(expense_repository)
    
    return {
        'auth': auth_service,
        'expense': expense_service,
        'categorization': categorization_service,
        'statistics': statistics_service,
        'user_repo': user_repository,
        'expense_repo': expense_repository,
        'category_repo': category_repository
    }


SERVICES = create_services()


class AppState:
    """Clase que maneja el estado de la aplicación para Gradio."""
    
    def __init__(self):
        self.current_user = None
        self.selected_year = datetime.now().year
        self.selected_month = datetime.now().month
    
    def is_authenticated(self) -> bool:
        return self.current_user is not None
    
    def get_user_id(self) -> str:
        return self.current_user.username if self.current_user else None
    
    def clear(self):
        self.current_user = None
        self.selected_year = datetime.now().year
        self.selected_month = datetime.now().month


APP_STATE = AppState()


def login_user(username: str, password: str, main_panel, auth_panel):
    """Maneja el login de usuario."""
    auth_service = SERVICES['auth']
    result = auth_service.login(username, password)
    
    if result.is_success:
        APP_STATE.current_user = result.data
        username_display = f"👤 {result.data.full_name}"
        return (
            gr.update(visible=True, elem_id="main_panel"),
            gr.update(visible=False),
            f"✅ ¡Bienvenido {result.data.full_name}!",
            username_display
        )
    return main_panel, auth_panel, "❌ Credenciales inválidas", ""


def register_user(full_name: str, username: str, password: str):
    """Maneja el registro de usuario."""
    auth_service = SERVICES['auth']
    result = auth_service.register(username, password, full_name)
    
    if result.is_success:
        return "✅ ¡Cuenta creada exitosamente! Ya puedes iniciar sesión."
    return f"❌ {result.error}"


def logout_user(main_panel, auth_panel):
    """Maneja el cierre de sesión."""
    auth_service = SERVICES['auth']
    auth_service.logout()
    APP_STATE.clear()
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        "",
        ""
    )


def add_expense(amount: float, date: datetime, description: str, category: str):
    """Registra un nuevo gasto."""
    if not APP_STATE.is_authenticated():
        return "❌ Debes iniciar sesión primero."
    
    expense_service = SERVICES['expense']
    result = expense_service.create_expense(
        user_id=APP_STATE.get_user_id(),
        description=description,
        amount=amount,
        date=date,
        category=category if category else None
    )
    
    if result.is_success:
        return "✅ Gasto registrado exitosamente."
    return f"❌ {result.error}"


def delete_expense(expense_id: str):
    """Elimina un gasto."""
    if not APP_STATE.is_authenticated():
        return "❌ Debes iniciar sesión primero."
    
    expense_service = SERVICES['expense']
    result = expense_service.delete_expense(expense_id, APP_STATE.get_user_id())
    
    if result.is_success:
        return gr.update(), get_expenses_data(), get_stats_data()
    return f"❌ {result.error}", gr.update(), gr.update()


def get_expenses_data():
    """Obtiene los datos de gastos para la tabla."""
    if not APP_STATE.is_authenticated():
        return []
    
    expense_service = SERVICES['expense']
    expenses = expense_service.get_user_expenses_for_period(
        APP_STATE.get_user_id(),
        APP_STATE.selected_year,
        APP_STATE.selected_month
    )
    
    data = []
    for exp in expenses:
        data.append([
            exp.id[:8],
            exp.date.strftime("%d/%m/%Y"),
            exp.description[:45] + "..." if len(exp.description) > 45 else exp.description,
            f"${exp.amount:,.2f}",
            exp.category,
            exp.id
        ])
    
    return data


def get_stats_data():
    """Obtiene los datos de estadísticas."""
    if not APP_STATE.is_authenticated():
        return 0, 0, 0, "N/A", gr.update()
    
    stats_service = SERVICES['statistics']
    summary = stats_service.get_statistics_summary(
        APP_STATE.get_user_id(),
        APP_STATE.selected_year,
        APP_STATE.selected_month
    )
    
    chart_data = stats_service.get_chart_data(
        APP_STATE.get_user_id(),
        APP_STATE.selected_year,
        APP_STATE.selected_month
    )
    
    pie_plot = create_pie_chart(chart_data)
    bar_plot = create_bar_chart(chart_data)
    
    top_cat = "N/A"
    if summary['top_category']:
        top_cat = f"{summary['top_category']['icon']} {summary['top_category']['name']}"
    
    return (
        summary['total'],
        summary['count'],
        summary['average'],
        top_cat,
        gr.update(value=pie_plot),
        gr.update(value=bar_plot)
    )


def create_pie_chart(chart_data: dict):
    """Crea un gráfico de pastel para la distribución por categoría."""
    if not chart_data['labels']:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        chart_data['values'],
        labels=chart_data['labels'],
        colors=chart_data['colors'],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title('Distribución por Categoría', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def create_bar_chart(chart_data: dict):
    """Crea un gráfico de barras para gastos por categoría."""
    if not chart_data['labels']:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    y_pos = range(len(chart_data['labels']))
    ax.barh(y_pos, chart_data['values'], color=chart_data['colors'])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(chart_data['labels'])
    ax.set_xlabel('Monto ($)', fontsize=10)
    ax.set_title('Gastos por Categoría', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig


def update_period(year: int, month: str):
    """Actualiza el período seleccionado."""
    month_num = MONTH_NAMES.index(month) + 1 if month in MONTH_NAMES else datetime.now().month
    APP_STATE.selected_year = year
    APP_STATE.selected_month = month_num
    return get_expenses_data(), get_stats_data()


def create_interface():
    """Crea la interfaz completa de Gradio."""
    
    with gr.Blocks(
        title="💰 Gestor de Gastos Personales",
        theme=gr.themes.Soft(
            primary_hue="teal",
            secondary_hue="gray"
        )
    ) as app:
        gr.Markdown("""
        # 💰 Gestor de Gastos Personales
        *Registra tus gastos, categorízalos automáticamente y visualiza tus estadísticas*
        """)
        
        with gr.Row():
            with gr.Column(scale=1, visible=True) as auth_panel:
                gr.Markdown("## 🔐 Acceso al Sistema")
                
                with gr.Tab("🔓 Iniciar Sesión"):
                    login_username = gr.Textbox(
                        label="Usuario",
                        placeholder="Ingresa tu nombre de usuario",
                        lines=1
                    )
                    login_password = gr.Textbox(
                        label="Contraseña",
                        type="password",
                        placeholder="Ingresa tu contraseña",
                        lines=1
                    )
                    login_btn = gr.Button("Entrar", variant="primary", scale=0)
                    login_output = gr.Textbox(
                        label="Estado",
                        interactive=False,
                        show_label=False
                    )
                
                with gr.Tab("📝 Registrarse"):
                    reg_fullname = gr.Textbox(
                        label="Nombre Completo",
                        placeholder="Tu nombre completo",
                        lines=1
                    )
                    reg_username = gr.Textbox(
                        label="Usuario",
                        placeholder="Elige un nombre de usuario",
                        lines=1
                    )
                    reg_password = gr.Textbox(
                        label="Contraseña",
                        type="password",
                        placeholder="Mínimo 4 caracteres",
                        lines=1
                    )
                    register_btn = gr.Button("Crear Cuenta", variant="primary", scale=0)
                    register_output = gr.Textbox(
                        label="Estado",
                        interactive=False,
                        show_label=False
                    )
                
                login_btn.click(
                    login_user,
                    inputs=[login_username, login_password, main_panel, auth_panel],
                    outputs=[main_panel, auth_panel, login_output, username_display]
                )
                
                register_btn.click(
                    register_user,
                    inputs=[reg_fullname, reg_username, reg_password],
                    outputs=[register_output]
                )
            
            with gr.Column(scale=2, visible=False) as main_panel:
                username_display = gr.Markdown("👤 Usuario")
                
                with gr.Row():
                    logout_btn = gr.Button("Cerrar Sesión", variant="secondary", size="sm")
                    logout_btn.click(
                        logout_user,
                        inputs=[main_panel, auth_panel],
                        outputs=[main_panel, auth_panel, login_output, username_display]
                    )
                
                gr.Markdown("---")
                
                with gr.Tabs():
                    with gr.Tab("📝 Registrar Gasto"):
                        gr.Markdown("### ➕ Nuevo Gasto")
                        
                        with gr.Row():
                            amount_input = gr.Number(
                                label="Monto *",
                                minimum=0.01,
                                precision=2,
                                scale=1
                            )
                            date_input = gr.DatePicker(
                                label="Fecha *",
                                max_date=datetime.now(),
                                scale=1
                            )
                            category_dd = gr.Dropdown(
                                label="Categoría (opcional)",
                                choices=[
                                    "Vivienda 🏠",
                                    "Alimentación 🍔",
                                    "Transporte 🚗",
                                    "Entretenimiento 🎮",
                                    "Compras 🛒",
                                    "Salud 💊",
                                    "Educación 📚",
                                    "Otros 💰"
                                ],
                                value=None,
                                scale=1
                            )
                        
                        desc_input = gr.Textbox(
                            label="Descripción",
                            placeholder="Ej: Compra en supermercado, Cena de trabajo...",
                            lines=2
                        )
                        
                        with gr.Row():
                            add_btn = gr.Button("💾 Guardar Gasto", variant="primary")
                            clear_btn = gr.Button("🔄 Limpiar", variant="secondary")
                        
                        add_output = gr.Textbox(
                            label="Estado",
                            interactive=False,
                            show_label=False
                        )
                        
                        def clear_form():
                            return 0, None, None, "", ""
                        
                        add_btn.click(
                            add_expense,
                            inputs=[amount_input, date_input, desc_input, category_dd],
                            outputs=[add_output]
                        )
                        
                        clear_btn.click(
                            clear_form,
                            outputs=[amount_input, date_input, category_dd, desc_input, add_output]
                        )
                    
                    with gr.Tab("📋 Ver Gastos"):
                        gr.Markdown("### 📊 Lista de Gastos")
                        
                        with gr.Row():
                            year_slider = gr.Dropdown(
                                label="Año",
                                choices=[str(y) for y in range(2020, 2031)],
                                value=str(APP_STATE.selected_year),
                                scale=1
                            )
                            month_dd = gr.Dropdown(
                                label="Mes",
                                choices=MONTH_NAMES,
                                value=MONTH_NAMES[APP_STATE.selected_month - 1],
                                scale=1
                            )
                            refresh_btn = gr.Button("🔄 Actualizar", variant="primary", scale=0)
                        
                        expenses_table = gr.Dataframe(
                            headers=["ID", "Fecha", "Descripción", "Monto", "Categoría", "ID_Gasto"],
                            datatype=["str", "str", "str", "str", "str", "str"],
                            interactive=False,
                            height=300
                        )
                        
                        def get_current_expenses():
                            return get_expenses_data()
                        
                        refresh_btn.click(
                            update_period,
                            inputs=[year_slider, month_dd],
                            outputs=[expenses_table, stat_total, stat_count, stat_avg, stat_top_cat, pie_chart, bar_chart]
                        )
                    
                    with gr.Tab("📈 Estadísticas"):
                        gr.Markdown("### 📊 Resumen de Gastos")
                        
                        with gr.Row():
                            with gr.Column(scale=1):
                                stat_total = gr.Number(label="💵 Total de Gastos", interactive=False)
                            with gr.Column(scale=1):
                                stat_count = gr.Number(label="📝 Transacciones", interactive=False)
                            with gr.Column(scale=1):
                                stat_avg = gr.Number(label="📊 Promedio por Gasto", interactive=False)
                            with gr.Column(scale=1):
                                stat_top_cat = gr.Textbox(label="🏆 Categoría Principal", interactive=False)
                        
                        gr.Markdown("### 📈 Visualización")
                        
                        with gr.Row():
                            with gr.Column(scale=1):
                                pie_chart = gr.Plot(label="Distribución por Categoría")
                            with gr.Column(scale=1):
                                bar_chart = gr.Plot(label="Gastos por Categoría")
                        
                        refresh_btn2 = gr.Button("🔄 Actualizar Estadísticas", variant="primary")
                        refresh_btn2.click(
                            get_stats_data,
                            outputs=[stat_total, stat_count, stat_avg, stat_top_cat, pie_chart, bar_chart]
                        )
        
        gr.Markdown("""
        ---
        *Prototipo de Gestión de Gastos Personales v1.0*
        
        **Nota:** Este es un prototipo funcional. Los datos se almacenan en memoria y se perderán
        al cerrar la aplicación.
        """)
    
    return app


def main():
    """Función principal de entrada."""
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
