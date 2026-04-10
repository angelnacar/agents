from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from agile_team.tools.custom_tool import FileWriterTool
from agile_team.schemas import (
    PRD, ArchitectureDesign, ImplementationOutput,
    SecurityReport, QAManifest, SprintReview
)
# from crewai.memory.storage import LTMSQLiteStorage, RAGStorage


@CrewBase
class AgileTeam():
    """AgileTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Initialize common tools
    file_writer = FileWriterTool()

    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'],
            verbose=True,
            allow_delegation=False,
            memory = True,
            tools=[self.file_writer]
        )

    @agent
    def tech_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_lead'],
            verbose=True,
            memory = True,
            allow_delegation=True,
            tools=[self.file_writer]
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            memory = True,
            tools=[self.file_writer],
            allow_delegation=False,
            max_execution_time=480, 
            max_retry_limit=5,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            memory = True,
            tools=[self.file_writer],
            allow_delegation=False,
            max_execution_time=480, 
            max_retry_limit=5,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'],
            verbose=True,
            memory = True,
            tools=[self.file_writer],
            allow_delegation=False,
            max_execution_time=480, 
            max_retry_limit=5,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],
            verbose=True,
            memory = True,
            tools=[self.file_writer],
            allow_delegation=False,
            max_execution_time=480, 
            max_retry_limit=5,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    @agent
    def scrum_master(self) -> Agent:
        return Agent(
            config=self.agents_config['scrum_master'],
            verbose=True,
            memory = True,
            allow_delegation=True,
          #  tools=[self.file_writer]
        )

    @task
    def requirement_definition(self) -> Task:
        return Task(
            config=self.tasks_config['requirement_definition']
         #   output_pydantic=PRD
        )

    @task
    def technical_architecture(self) -> Task:
        return Task(
            config=self.tasks_config['technical_architecture']
        )

    @task
    def backend_development(self) -> Task:
        return Task(
            config=self.tasks_config['backend_development']
        )

    @task
    def frontend_development(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_development']
        )

    @task
    def security_audit(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit']
         #   output_pydantic=SecurityReport
        )

    @task
    def quality_assurance(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance']
         #   output_pydantic=QAManifest
        )

    @task
    def sprint_review(self) -> Task:
        return Task(
            config=self.tasks_config['sprint_review']
         #   output_pydantic=SprintReview
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgileTeam crew"""
        # Filtramos la lista de agentes para quitar al scrum_master ya que será el manager_agent
        # Esto evita el error: "Manager agent should not be included in agents list"
        filtered_agents = [agent for agent in self.agents if agent != self.scrum_master()]

        return Crew(
            agents=filtered_agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.scrum_master(),
            memory=True,
            verbose=True,
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )
       # )
        # return Crew(
        #     agents=self.agents,
        #     tasks=self.tasks,
        #     process=Process.hierarchical,
        #     manager_agent=manager,
        #     memory=True,
        #     long_term_memory = long_term_memory,
        #     short_term_memory = short_term_memory,            
        #     entity_memory = entity_memory,
        #     verbose=True
        # )
