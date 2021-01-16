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

    def __init__(
            self,
            number_agents,
            width,
            height,
            sick_p=0.2,
            aymp_p=0.2,
            imr_immune_p=0.2,
            imr_asymp_p=0.2,
            imr_mod_p=0.2,
            imr_severe_p=0.2,
            imr_dead_p=0.2,
            wearing_mask=0.2,
            travelling_agents=10,
            vaccination_prcntg=0.1,
            static=False
    ) -> None:
        """Simulation constructor.

        Args:
            number_agents (Integer): Number of Agents. in the model.
            width (Integer): Simulation's width.
            height (Integer): Simulation's height.
            sick_p (float, optional): Percentage of infected (sick) agents. Defaults to 0.2.
            aymp_p (float, optional): Percentage of infected (asymptomatic)agents. Defaults to 0.2.
            imr_immune_p (float, optional): Percentage of agents for immune IMR. Defaults to 0.2.
            imr_asymp_p (float, optional): Percentage of agents for asymptomatic IMR. Defaults to 0.2.
            imr_mod_p (float, optional): Percentage of agents for moderately infected IMR. Defaults to 0.2.
            imr_severe_p (float, optional): Percentage of agents for severe infected IMR. Defaults to 0.2.
            imr_dead_p (float, optional): Percentage of agents for deadly IMR. Defaults to 0.2.
            wearing_mask (float, optional): Percentage of agents wearing a mask. Defaults to 0.2.
            travelling_agents (Integer, optional): Max number of agents Travelling in each day. Defaults to 10.
            vaccination_prcntg (float, optional): Percentage of agents being vaccinated in each day. Defaults to 0.1.
            static (bool, optional): If the simulation will have a static beginning. Defaults to False.
        """
        self.num_agents = number_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.quarantine_list = []
        self.daily_infected = 0
        self.daily_recovered = 0
        self.daily_dead = 0
        self.daily_quarantine = 0

        self.sick_p = sick_p
        self.aymp_p = aymp_p
        self.imr_immune_p = imr_immune_p
        self.imr_asymp_p = imr_asymp_p
        self.imr_mod_p = imr_mod_p
        self.imr_severe_p = imr_severe_p
        self.imr_dead_p = imr_dead_p
        self.wearing_mask = wearing_mask

        travel_max = int(number_agents * 0.2)
        if travelling_agents > travel_max:
            logger.warning(
                f'Allowed number of travelling agents exceeded! Default number will be used : {travel_max} ')
            travelling_agents = travel_max

        self.travelling_agents_nbr = travelling_agents
        self.vaccination_nbr = int(number_agents * vaccination_prcntg)
        self.totals_dict = {
            "Recovered Agents": 0,
            "Dead Agents": 0,
            "Healthy Agents": 0
        }

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
            hs_data, imr_data, mask_data = self.get_static_data()

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
        self.datacollector_currents_prcntg = DataCollector(
            {"Sick Agents": SimulationModel.current_values_sick,
             "Recovered Agents": SimulationModel.current_values_recover,
             "Dead Agents": SimulationModel.current_values_dead,
             "Healthy Agents": SimulationModel.current_values_healthy,
             "Quarantine Agents": SimulationModel.current_values_quarantine})

        # data collect to build the chart
        self.datacollector_dailys = DataCollector(
            {"Infected Agents": SimulationModel.daily_values_sick,
             "Recovered Agents": SimulationModel.daily_values_recover,
             "Dead Agents": SimulationModel.daily_values_dead,
             "Quarantine Agents": SimulationModel.daily_values_quarantine})

        # data collect to build the chart
        self.datacollector_cumulatives_prcntg = DataCollector(
            {"Recovered Agents": SimulationModel.cumulative_values_recover_prcntg,
             "Dead Agents": SimulationModel.cumulative_values_dead_prcntg,
             "Healthy Agents": SimulationModel.cumulative_values_healthy_prcntg})

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

        self.remove_dead_agents()  # I do not know why, but we cannot remove the dead agents after calling the setp method. Otherwise the chart of dead people will have no values

        self.check_simulation_end()

        self.schedule.step()  # does the simulation step

        # Quarantine zone update
        if self.schedule.steps >= constants.QUARANTINE_DAYS:
            self.update_quarantine_health_status()
            self.update_quarantine()
            if self.vaccination_nbr > 0:
                self.update_quarantine_vaccinated_agents()

        # vaccinate agents
        if self.vaccination_nbr > 0:
            self.vaccination()

        # collecting data for chart
        self.datacollector_currents_prcntg.collect(self)
        self.datacollector_cumulatives_prcntg.collect(self)
        self.datacollector_dailys.collect(self)

        # reset daily counters
        self.reset_daily_data()

        # adding travelling agents
        if self.travelling_agents_nbr > 0:
            self.travelling()

        if not self.running:
            logger.info(
                f'Total number of immune people: {SimulationModel.final_immune_nbr(self)}')

    def vaccination(self) -> None:
        """Vaccinates the agents
        """
        for agent in SimulationModel.get_healthy_no_immune_agents(self)[:self.vaccination_nbr]:
            agent.vaccinated = 1
            logger.info(
                f'Agent {agent.unique_id} got his first vaccine dose! Step: {self.schedule.steps}')
            # updates the vacination days in the agent health status update

    def travelling(self) -> None:
        """Adds an removes new agents from the model, simulating the travelling behaviour.
        """
        self.removing_travelling_agents()
        self.add_travelling_agents()

    def add_travelling_agents(self) -> None:
        """Adds new agents into the model, simulating the travelling behaviour when people arrive in our city.
        The arriving agents have random status.
        So, they can be infected and infect other agents or be healthy and got infected.
        """
        for i in range(random.randint(0, self.travelling_agents_nbr)):
            agent = SimulationAgent(model=self)
            self.schedule.add(agent)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            logger.info(
                (f'Agent {agent.unique_id} arrived! He is {constants.HEALTH_STATUS_DICT[agent.health_status]} and he {"wears" if agent.wear_mask else "does not wear"}'
                 f' a mask. He have a vaccinated value of {agent.vaccinated}'))

    def removing_travelling_agents(self) -> None:
        """Removes agents from the model, simulating the travelling behaviour when people go to another place.
        """
        for i in range(random.randint(0, self.travelling_agents_nbr)):
            agent = self.schedule.agents[random.randint(
                0, len(self.schedule.agents)-1)]
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            logger.debug(
                f'Agent {agent.unique_id} left the city! He is {constants.HEALTH_STATUS_DICT[agent.health_status]} and he {"wears" if agent.wear_mask else "does not wear"} a mask')

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
                # only counting here as in the step the models updates the counter with the grid agents
                self.daily_dead += 1

    def update_quarantine_vaccinated_agents(self) -> None:
        """For each agent in quarantine updates the vaccination status.
        """
        for agent in self.quarantine_list:
            SimulationAgent.update_vaccinated_agents(agent)

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
            self.daily_quarantine += 1
            # saving agents removed from grid to add them as soon as they get healed
            logger.debug(f"Agent {agent.unique_id} is now in quarantine. ")

        # removing healed people from quarantine (dead are removed before in the step method)
        for index, agent in enumerate(self.quarantine_list):
            if agent.health_status > constants.ASYMPTOMATIC:
                self.quarantine_list.pop(index)
                self.schedule.add(agent)
                # Add the agent to a random grid cell
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(agent, (x, y))
                self.daily_quarantine -= 1
                # self.daily_recovered += 1 #update_infected_agents already sets the revocered agent to the counter

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

    def get_static_data(self) -> tuple:
        """Returns the lists of static data to initialize the agents based on the configurations file.

        Returns:
            (tuple): hs_data, imr_data, mask_data.
        """
        if math.ceil(sum([self.imr_immune_p, self.imr_asymp_p, self.imr_mod_p, self.imr_severe_p, self.imr_dead_p])) != 1:
            sys.exit(
                f"IMMMUNE_IMR_PRCNTG + ASYMP_IMR_PRCNTG + MOD_IMR_PRCNTG + SEVERE_IMR_PRCNTG + DEAD_IMR_PRCNTG must sum to 1, got {sum([self.imr_immune_p, self.imr_asymp_p, self.imr_mod_p, self.imr_severe_p, self.imr_dead_p])}")

        healty_agents = self.num_agents - \
            ((self.num_agents * self.sick_p) +
             (self.num_agents * self.aymp_p))
        # immune people are healthy
        if healty_agents < (self.num_agents * constants.IMMMUNE_IMR_PRCNTG):
            logging.error(
                f"The number of HEALTHY agents ({healty_agents}) cannot be less than the number of immune agents ({constants.IMMMUNE_IMR_PRCNTG})")
            sys.exit()

        hs_data, imr_data, mask_data = utils.static_simulation(self.num_agents, self.sick_p, self.aymp_p, self.imr_immune_p,
                                                               self.imr_asymp_p, self.imr_mod_p, self.imr_severe_p, self.imr_dead_p,
                                                               self.wearing_mask)
        if len(hs_data) != self.num_agents or len(imr_data) != self.num_agents:
            logging.error(
                f"The number of HEALTH STATUS ({len(hs_data)}) and IMR ({len(imr_data)}) data must be equal to the Total of AGENTS in the simulation ({constants.TOTAL_NUMBER_OF_AGENTS})")
            sys.exit()

        return hs_data, imr_data, mask_data

    def reset_daily_data(self) -> None:
        """Resets the daily total to "0"

        """
        self.daily_infected = 0
        self.daily_recovered = 0
        self.daily_dead = 0
        self.daily_quarantine = 0

    @ staticmethod
    def get_healthy_no_immune_agents(model) -> list:
        """Returns the list of healthy agents, not vaccinated, with a immune system response of not immune.

        Args:
            model (SimulationModel): The model instance

        Returns:
            list: List of agents
        """
        return [agent for agent in model.schedule.agents if agent.health_status == constants.HEALTHY and
                agent.immune_system_response != constants.IMR_IMMUNE and not agent.vaccinated]

    @ staticmethod
    def current_values_sick(model) -> int:
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

    @ staticmethod
    def current_values_recover(model) -> int:
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

        model.totals_dict["Recovered Agents"] = cumulative_recovery

        return cumulative_recovery

    @ staticmethod
    def current_values_dead(model) -> int:
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

        model.totals_dict["Dead Agents"] += cumulative_dead

        return cumulative_dead

    @ staticmethod
    def current_values_healthy(model) -> int:
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

        model.totals_dict["Healthy Agents"] = cumulative_healthy

        return cumulative_healthy

    @ staticmethod
    def current_values_quarantine(model) -> int:
        """Returns the total number of agents in the quarantine zone.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return len(model.quarantine_list)

    @ staticmethod
    def daily_values_sick(model) -> int:
        """Returns the daily total number of SICK and ASYMPTOMATIC agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.daily_infected

    @ staticmethod
    def daily_values_recover(model) -> int:
        """Returns the daily total number of recovered agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.daily_recovered

    @ staticmethod
    def daily_values_dead(model) -> int:
        """Returns the daily total number of DEAD agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.daily_dead

    @ staticmethod
    def daily_values_quarantine(model) -> int:
        """Returns the daily total number of agents in the quarantine zone.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.daily_quarantine

    @ staticmethod
    def cumulative_values_recover_prcntg(model) -> int:
        """Returns the cumulative total of recovered agents during the whole simulation.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.totals_dict["Recovered Agents"]

    @ staticmethod
    def cumulative_values_dead_prcntg(model) -> int:
        """Returns the cumulative total of DEAD agents during the whole simulation.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.totals_dict["Dead Agents"]

    @ staticmethod
    def cumulative_values_healthy_prcntg(model) -> int:
        """Returns the cumulative total of DEAD agents during the whole simulation.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return model.totals_dict["Healthy Agents"]

    @ staticmethod
    def final_immune_nbr(model) -> int:
        """Returns the final number of immune agents (includes vaccination and getting sick).

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        IMR = [agent for agent in model.schedule.agents if agent.immune_system_response ==
               constants.IMR_IMMUNE]
        return len(IMR)


if __name__ == "__main__":
    pass
