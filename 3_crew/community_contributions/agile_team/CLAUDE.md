# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Run the crew**: `crewai run`
- **Install dependencies**: `crewai install`
- **Training**: Defined in `src/agile_team/main.py` as `train()`.
- **Testing**: Defined in `src/agile_team/main.py` as `test()`.
- **Replay**: Defined in `src/agile_team/main.py` as `replay()`.

## Architecture and Structure

The project is built using the `crewAI` framework for multi-agent orchestration.

### Core Components
- **Crew Definition**: `src/agile_team/crew.py` - Defines the `AgileTeam` class, decorators for agents and tasks, and the crew assembly (sequential process).
- **Execution Entrypoint**: `src/agile_team/main.py` - Contains the `run()` function and other utility functions (`train`, `replay`, `test`) to execute the crew locally with specific inputs.
- **Configuration**:
    - `src/agile_team/config/agents.yaml`: Defines agent roles, goals, and backstories.
    - `src/agile_team/config/tasks.yaml`: Defines task descriptions and expected outputs.
- **Custom Tools**: `src/agile_team/tools/` - Location for adding custom tools available to agents.

### Logic Flow
1. `main.py` provides inputs (e.g., `topic`, `current_year`).
2. `crew.py` initializes agents and tasks using configurations from YAML files.
3. The `Crew` executes the tasks sequentially, passing the output of the `researcher` to the `reporting_analyst`.
4. The final output is written to `report.md`.
