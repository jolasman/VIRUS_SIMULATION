from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid  # allows multiple agents in the same cell
from mesa.datacollection import DataCollector
from mesa_agent import SimulationAgent
import constants
import random
import logging

logging.basicConfig(
    level=constants.LOG_LEVEL,
    filename='logs/mesa_model.log',
    filemode='w',
    format="%(name)s %(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


class SimulationModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        print("init called")
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        dead = 0
        for i in range(self.num_agents):
            agent = SimulationAgent(model=self)
            if agent.immune_system_response == constants.IMR_DEADLY_INFECTED:
                dead += 1
            self.schedule.add(agent)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        logger.info(f"dead number : {dead}")
        print(dead)

        self.datacollector_sick = DataCollector(
            model_reporters={"Sick Agents": cumulative_values_sick})
        self.datacollector_recover = DataCollector(
            model_reporters={"Recovered Agents": cumulative_values_recover})
        self.datacollector_dead = DataCollector(
            model_reporters={"Dead Agents": cumulative_values_dead})
        self.datacollector_healthy = DataCollector(
            model_reporters={"Healthy Agents": cumulative_values_healthy})

    def remove_dead(self):
        """Removes the dead agents from the simulation
        """
        for agent in self.schedule.agents:
            if agent.health_status == constants.DEAD:
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)

    def check_simulation_end(self):
        """Stops the simulation when the it does not have more infected agents
        """
        # if there is any agent in the list that is sickl or asymptomatic
        if not any(agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC for agent in self.schedule.agents):
            self.running = False

    def step(self):
        """[summary]
        """
        self.datacollector_sick.collect(self)
        self.datacollector_recover.collect(self)
        self.datacollector_dead.collect(self)
        self.datacollector_healthy.collect(self)
        self.remove_dead()  # I do not now why, but we cannot remove the dead agents after calling the setp method. Otherwise the chart of dead people will have no values
        self.schedule.step()
        self.check_simulation_end()


def cumulative_values_sick(model):
    cumulative_sick = 0
    for agent in model.schedule.agents:
        if agent.health_status == constants.SICK:
            cumulative_sick += 1
        if agent.health_status == constants.ASYMPTOMATIC:
            cumulative_sick += 1

    return cumulative_sick


def cumulative_values_recover(model):
    cumulative_recovery = 0
    for agent in model.schedule.agents:
        if agent.health_status == constants.TOTAL_RECOVERY:
            cumulative_recovery += 1
        if agent.health_status == constants.WITH_DISEASES_SEQUELAES:
            cumulative_recovery += 1

    return cumulative_recovery


def cumulative_values_dead(model):
    cumulative_dead = 0
    for agent in model.schedule.agents:
        if agent.health_status == constants.DEAD:
            cumulative_dead += 1

    return cumulative_dead


def cumulative_values_healthy(model):
    cumulative_healthy = 0
    for agent in model.schedule.agents:
        if agent.health_status == constants.HEALTHY:
            cumulative_healthy += 1

    return cumulative_healthy


if __name__ == "__main__":
    pass