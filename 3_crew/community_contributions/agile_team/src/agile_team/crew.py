from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from agile_team.tools.custom_tool import FileWriterTool
from agile_team.schemas import (
    PRD, ArchitectureDesign, ImplementationOutput,
    SecurityReport, QAManifest, SprintReview
)

@CrewBase
class AgileTeam():
    """AgileTeam crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Initialize common tools
    file_writer = FileWriterTool()

    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'],
            verbose=True,
            tools=[self.file_writer]
        )

    @agent
    def tech_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_lead'],
            verbose=True,
            tools=[self.file_writer]
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            tools=[self.file_writer],
            code_execution_mode="safe"
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            tools=[self.file_writer],
            code_execution_mode="safe"
        )

    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            verbose=True,
            tools=[self.file_writer],
            code_execution_mode="safe"
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],
            verbose=True,
            tools=[self.file_writer],
            code_execution_mode="safe"
        )

    @agent
    def scrum_master(self) -> Agent:
        return Agent(
            config=self.agents_config['scrum_master'],
            verbose=True,
            tools=[self.file_writer]
        )

    @task
    def requirement_definition(self) -> Task:
        return Task(
            config=self.tasks_config['requirement_definition'],
            output_pydantic=PRD
        )

    @task
    def technical_architecture(self) -> Task:
        return Task(
            config=self.tasks_config['technical_architecture'],
            output_pydantic=ArchitectureDesign
        )

    @task
    def backend_development(self) -> Task:
        return Task(
            config=self.tasks_config['backend_development'],
            output_pydantic=ImplementationOutput
        )

    @task
    def frontend_development(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_development'],
            output_pydantic=ImplementationOutput
        )

    @task
    def security_audit(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit'],
            output_pydantic=SecurityReport
        )

    @task
    def quality_assurance(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance'],
            output_pydantic=QAManifest
        )

    @task
    def sprint_review(self) -> Task:
        return Task(
            config=self.tasks_config['sprint_review'],
            output_pydantic=SprintReview
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgileTeam crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
