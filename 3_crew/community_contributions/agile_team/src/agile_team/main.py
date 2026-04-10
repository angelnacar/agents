#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from agile_team.crew import AgileTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    initial_requirements = """Un prototipo de una aplicación de gastos personales que permita un logueo sencillo, registro de gastos, categorización automática de los mismos y visualización de estadísticas mensuales. 
    El prototipo debe incluir una interfaz de usuario básica y una estructura de backend que permita la escalabilidad futura del proyecto.
    Por ahora el usuario sólo quiere un pequeño prototipo de uso. Nada de implementar acceso a base de datos ni nada por el estilo. Solo un prototipo funcional que pueda mostrar a sus jefes la idea.
    El prototipo debe ser desarrollado utilizando Python para el backend y Gradio para el frontend."""


    module_name = "personal_account.py"
    interface_name = "ui.py"

    inputs = {
        'initial_requirements': initial_requirements,
        'module_name': module_name,
        'interface_name': interface_name
    }

    try:
        AgileTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
