import math
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid  # allows multiple agents in the same cell
from mesa.datacollection import DataCollector
from mesa_agent import SimulationAgent
import constants
import random
import logging
import sys
import utils

logging.basicConfig(
    level=constants.LOG_LEVEL,
    filename='logs/mesa_model.log',
    filemode='w',
    format="%(name)s %(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)


class SimulationModel(Model):
    """Class representing the simulation's model."""

    def __init__(self, N, width, height, static=False) -> None:
        """Simulation constructor.

        Args:
            N (Integer): Number of Agents. in the model.
            width (Integer): Simulation's width.
            height (Integer): Simulation's height.
            random (bool, optional): If the agents will have random parameters. Defaults to False.
        """
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.quarantine_list = []

        if not static:
            # Create agents
            for i in range(self.num_agents):
                agent = SimulationAgent(model=self)
                self.schedule.add(agent)
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))
        else:
            hs_data, imr_data, mask_data = SimulationModel.get_static_data()

            for i in range(self.num_agents):
                agent = SimulationAgent(model=self, health_status=hs_data.pop(), immune_system_response=imr_data.pop(),
                                        wear_mask=mask_data.pop())
                # adding the agent to the schedule so we can activate it using the step method
                self.schedule.add(agent)

                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

                self.grid.place_agent(agent, (x, y))
                
        # data collect to build the chart
        self.datacollector_cumulatives = DataCollector(
            {"Sick Agents": SimulationModel.cumulative_values_sick,
             "Recovered Agents": SimulationModel.cumulative_values_recover,
             "Dead Agents": SimulationModel.cumulative_values_dead,
             "Healthy Agents": SimulationModel.cumulative_values_healthy,
             "Quarantine Agents": SimulationModel.cumulative_values_quarantine})

    def step(self) -> None:
        """Performs the simulation's step by activating each agents step method.
        
        This method also removes the dead agents, updates the quarantine zone, collects the chart data, and validates if the simulation achieved its goal.
        """
        if self.schedule.steps == 0:
            infected, healthy = self.get_totals_health_status()
            logger.info(
                f"Number of:  infected agents --> {infected} -  Healthy agents --> {healthy}")
            logger.info(
                f"Number of deadly infected agents: {self.get_imr_deadly()}")
        
        # collecting data for chart    
        self.datacollector_cumulatives.collect(self)

        self.remove_dead_agents()  # I do not know why, but we cannot remove the dead agents after calling the setp method. Otherwise the chart of dead people will have no values
        self.schedule.step() # do the simulation step
        
        #Quarantine zone update
        if self.schedule.steps >= constants.QUARANTINE_DAYS:
            self.update_quarantine_health_status()
            self.update_quarantine()
        self.check_simulation_end()

    def remove_dead_agents(self) -> None:
        """Removes the dead agents from the simulation.
        """
        # if it is in the grid
        for env_agent in self.schedule.agents:
            if env_agent.health_status == constants.DEAD:
                self.grid.remove_agent(env_agent)
                self.schedule.remove(env_agent)
        # if in quarentine
        for quaran_index, quaran_agent in enumerate(self.quarantine_list):
            if quaran_agent.health_status == constants.DEAD:
                self.quarantine_list.pop(quaran_index)

    def update_quarantine_health_status(self) -> None:
        """For each agent in quarantine we check is health and update is value based on the number of days with the virus.
        """
        for agent in self.quarantine_list:
            SimulationAgent.update_infected_agents(agent)

    def update_quarantine(self) -> None:
        """Adds or removes agents from quarantine.
        """
        infected_list = [agent for agent in self.schedule.agents if agent.health_status ==
                         constants.SICK or agent.health_status == constants.ASYMPTOMATIC]
        # only a percentage of agents go to quarantine, the others remain indetected by autorities
        for agent in infected_list[:math.ceil(len(infected_list) * constants.QUARANTINE_PERCENTAGE)]:
            # quarantine zone
            self.quarantine_list.append(agent)
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            #self.daily_quarantine += 1
            # saving agents removed from grid to add them as soon as they get healed
            logger.debug(f"Agent {agent.unique_id} is now in quarantine. ")

        # removing healed people from quarantine
        for index, agent in enumerate(self.quarantine_list):
            if agent.health_status > constants.ASYMPTOMATIC:
                self.quarantine_list.pop(index)
                self.schedule.add(agent)
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))
                #self.daily_quarantine -= 1
                logger.debug(
                    f"Agent {agent.unique_id} is now with good health. The agents is now returning to the grid at {agent.pos}")

    def check_simulation_end(self) -> None:
        """Stops the simulation when it does not have more infected agents (in both, grid and quarantine).
        """
        # if there is any agent in the list that is sickl or asymptomatic
        if not any(agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC for agent in self.schedule.agents) and \
                not any(agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC for agent in self.quarantine_list):
            self.running = False

    def get_totals_health_status(self) -> tuple:
        """Returns the total number of infected, healthy agents in the current step.

        Returns:
            [Pack/Tuple](Integer): infected, healthy.
        """
        infected = healthy = 0
        for agent in self.schedule.agents:
            if agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC:
                infected += 1
            elif agent.health_status == constants.HEALTHY:
                healthy += 1

        return infected, healthy

    def get_imr_deadly(self) -> int:
        """Returns the total number of agents with immune system response of deadly infected.

        Returns:
            (Integer): Number of deadly infected.
        """
        deadly = [1 for agent in self.schedule.agents if agent.immune_system_response ==
                  constants.IMR_DEADLY_INFECTED]

        return len(deadly)


    @staticmethod
    def cumulative_values_sick(model) -> int:
        """Returns the total number of SICK and ASYMPTOMATIC agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        cumulative_sick = 0
        for agent in model.schedule.agents:
            if agent.health_status == constants.SICK:
                cumulative_sick += 1
            if agent.health_status == constants.ASYMPTOMATIC:
                cumulative_sick += 1
        for agent in model.quarantine_list:
            if agent.health_status == constants.SICK:
                cumulative_sick += 1
            if agent.health_status == constants.ASYMPTOMATIC:
                cumulative_sick += 1

        return cumulative_sick


    @staticmethod
    def cumulative_values_recover(model) -> int:
        """Returns the total number of TOTAL_RECOVERY and WITH_DISEASES_SEQUELAES agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        cumulative_recovery = 0
        for agent in model.schedule.agents:
            if agent.health_status == constants.TOTAL_RECOVERY:
                cumulative_recovery += 1
            if agent.health_status == constants.WITH_DISEASES_SEQUELAES:
                cumulative_recovery += 1

        return cumulative_recovery


    @staticmethod
    def cumulative_values_dead(model) -> int:
        """Returns the total number of DEAD agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        cumulative_dead = 0
        for agent in model.schedule.agents:
            if agent.health_status == constants.DEAD:
                cumulative_dead += 1
        for agent in model.quarantine_list:
            if agent.health_status == constants.DEAD:
                cumulative_dead += 1

        return cumulative_dead


    @staticmethod
    def cumulative_values_healthy(model) -> int:
        """Returns the total number of HEALTHY agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        cumulative_healthy = 0
        for agent in model.schedule.agents:
            if agent.health_status == constants.HEALTHY:
                cumulative_healthy += 1

        return cumulative_healthy


    @staticmethod
    def cumulative_values_quarantine(model) -> int:
        """Returns the total number of agents in the quarantine zone.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return len(model.quarantine_list)


    @staticmethod
    def get_static_data() -> tuple:
        """Returns the lists of static data to initialize the agents based on the configurations file.

        Returns:
            (tuple): hs_data, imr_data, mask_data.
        """
        healty_agents = constants.TOTAL_NUMBER_OF_AGENTS - \
            (constants.SICK_NBR + constants.ASYMP_NBR)
        if healty_agents < constants.IMMMUNE_IMR_NBR:  # immune people are healthy
            logging.error(
                f"The number of HEALTHY agents ({healty_agents}) cannot be less than the number of immune agents ({constants.IMMMUNE_IMR_NBR})")
            sys.exit()

        hs_data, imr_data, mask_data = utils.static_simulation(
            constants.SICK_NBR, constants.ASYMP_NBR, constants.IMMMUNE_IMR_NBR, constants.ASYMP_IMR_NBR, constants.MOD_IMR_NBR, constants.HIGH_IMR_NBR, constants.DEAD_IMR_NBR, constants.AGENTS_WEARING_MASK)
        if len(hs_data) != constants.TOTAL_NUMBER_OF_AGENTS or len(imr_data) != constants.TOTAL_NUMBER_OF_AGENTS:
            logging.error(
                f"The number of HEALTH STATUS ({len(hs_data)}) and IMR ({len(imr_data)}) data must be equal to the Total of AGENTS in the simulation ({constants.TOTAL_NUMBER_OF_AGENTS})")
            sys.exit()

        return hs_data, imr_data, mask_data


if __name__ == "__main__":
    pass
