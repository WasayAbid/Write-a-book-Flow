from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BookWriterCrew:
    """Book Writer Crew"""

    # Define the YAML configuration files for agents and tasks
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Defining the agents and their configurations
    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
        )

    @agent
    def outline_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["outline_agent"],
        )

    @agent
    def writing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["writing_agent"],
        )

    @agent
    def editing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["editing_agent"],
        )

    # Defining the tasks and their configurations
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def outline_task(self) -> Task:
        return Task(
            config=self.tasks_config["outline_task"],
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["writing_task"],
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config["editing_task"],
        )

    # Defining the crew with sequential task execution
    @crew
    def crew(self) -> Crew:
        """Creates the Book Writing Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
