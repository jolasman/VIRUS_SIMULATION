import logging
from mesa import Agent
import constants
import uuid
import random
from faker import Faker
fake = Faker()
logging.basicConfig(
    level=constants.LOG_LEVEL,
    filename='logs/mesa_model.log',
    filemode='w',
    format="%(name)s %(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)

days_list = [i for i in range(0, 21)]  # 21 as the second dose
days_list.append(False)


class SimulationAgent(Agent):
    """Class representing a human being (Agent).
    """

    def __init__(self, model,  name=None, age=None, health_status=None, immune_system_response=None, wear_mask=None) -> None:
        """Class constructor.

        Args:
            model (mesa.Model): The simulation's model.
            name (str, optional): Agent's name. Defaults to None.
            age (Integer, optional): Agent's age. Defaults to None.
            health_status (inIntegert, optional): Agent's health status. Defaults to None.
            immune_system_response (Integer, optional): Agent's Immune System response type. Defaults to None.
            wear_mask (Boolean, optional): If agent wears a mask. Defaults to None.
        """
        id_ = uuid.uuid1()
        super().__init__(id_, model)
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = fake.name()

        if health_status is None:
            health_status = random.choice([constants.SICK,
                                           constants.ASYMPTOMATIC,
                                           constants.WITH_DISEASES_SEQUELAES,
                                           constants.TOTAL_RECOVERY,
                                           constants.HEALTHY
                                           ])

        if immune_system_response is None:
            immune_system_response = SimulationAgent.immune_response_by_age(
                age, health_status)

        if wear_mask is None:
            wear_mask = bool(random.getrandbits(1))

        self.name = name
        self.age = age
        self.health_status = health_status
        self.previous_health_status = None
        self.immune_system_response = immune_system_response
        self.infected_days = None
        self.recovered = False
        self.wear_mask = wear_mask
        self.quarantine = False
        self.vaccinated = random.choice(days_list) if self.immune_system_response != constants.IMR_IMMUNE \
            and self.health_status == constants.HEALTHY else True

    def move(self) -> None:
        """This methods allows the agent to move into a new grid cell.
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            # If True, may move in all 8 directions.Otherwise, only up, down, left, right.
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def move_social_distance(self) -> None:
        """This methods allows the agent to move into a new grid cell.
        """
        possible_new_pos = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        new_position = None
        tries = 0  # number of times the agent tries to keep the social distance until quit
        random.shuffle(possible_new_pos)

        # start while
        # checking if agent can move to a cell in the neighborhood based on the social distance value for each cell
        while new_position is None and tries < constants.SOCIAL_DISTANCE_TRIES:
            tries += 1
            logger.debug(
                f'Agent {self.unique_id} try number {tries}!')
            for pos in possible_new_pos:
                cells_in_neighborhood = self.model.grid.get_neighborhood(
                    pos,
                    # If True, may move in all 8 directions.Otherwise, only up, down, left, right.
                    moore=True,
                    include_center=False,
                    radius=constants.SOCIAL_DISTANCE_STEP)
                logger.debug(
                    f'Agent {self.unique_id} cells_in_neighborhood: {cells_in_neighborhood}!')

                # if no cell with agents in the neighborhood (empty cell), the current agents cell is not empty for all neighborhood checks
                if [self.model.grid.is_cell_empty(cell) for cell in cells_in_neighborhood].count(False) == 1:
                    new_position = self.random.choice(cells_in_neighborhood)

            # trying another cell
            if new_position is None:
                possible_new_pos = self.model.grid.get_neighborhood(
                    # getting random empty cell
                    self.random.choice(
                        sorted(self.model.grid.empties, reverse=True)),
                    moore=True,
                    include_center=False)
                logger.debug(
                    f'Agent {self.unique_id} new possible cells: {possible_new_pos}!')
        # end while

        # moves agent if there is no agents in the social distance radius
        if new_position:
            logger.debug(
                f'Agent {self.unique_id} got a new cell keeping the social distance: {new_position}')
            self.model.grid.move_agent(self, new_position)
        else:  # the agent can stay or move to a random empty cell, like i quit this sh!t!
            value = random.random()
            if value <= 0.5:
                new_position = self.random.choice(
                    sorted(self.model.grid.empties))

                self.model.grid.move_agent(self, new_position)
                logger.debug(
                    f'Agent {self.unique_id} gave up on applying the social distance: {new_position} {self.model.grid.is_cell_empty(new_position)}')
            else:
                logger.debug(
                    f'Agent {self.unique_id} will not move because he is concerned to keep the social distance!')

    def agents_in_contact(self) -> None:
        """Updates the status for each agent when in contact with other agents.
        """
        # getting cell in the contagious radius
        cells_in_neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            # If True, may move in all 8 directions.Otherwise, only up, down, left, right.
            moore=True,
            # still using multigrid , so more than one agent cann be in the same cell
            include_center=True,
            radius=constants.CONTAGIOUS_DISTANCE)

        # getting the agents inside the cells
        cellmates = []
        for cell in cells_in_neighborhood:
            tmp_cellmates = self.model.grid.get_cell_list_contents([cell])
            for mate in tmp_cellmates:
                cellmates.append(mate)

        # if there is agents in contact
        if len(cellmates) > 1:
            for agent in cellmates:
                # excluding the day 0, when the agents get the infection, where we change from None to 0
                if agent != self and agent.infected_days and not self.recovered:
                    # can get the virus, neverthless he got it once before, the recovered instance variable can change
                    if self.health_status > constants.ASYMPTOMATIC:
                        hs_new_value_for_current_agent = SimulationAgent.value_based_probability(
                            agent.health_status, self.immune_system_response, agent.wear_mask, self.wear_mask)
                        if hs_new_value_for_current_agent != -1:
                            self.health_status = hs_new_value_for_current_agent
                            logger.debug(
                                f"Agent {self.unique_id} had an update in his health status: {constants.HEALTH_STATUS_DICT[self.health_status]}")

    def step(self) -> None:
        """Executes the agent actions in each sumulation step.

        First it moves the agent, then evaluates the other agents in contact with it. 
        Finally, the "clinic" situation of the agent is updated, based on the number days with the virus and the agents parameters.
        """
        if constants.SOCIAL_DISTANCE_STEP == 0:
            self.move()
        else:
            self.move_social_distance()

        self.agents_in_contact()
        self.update_infected_agents_env()
        self.update_vaccinated_agents_env()

    def get_health_status(self) -> int:
        """Return the agent's healt_status.

        Returns:
            (Integer): Agent's healt_status.
        """
        return self.health_status

    def update_infected_agents_env(self) -> None:
        """Updates the agents health status based on the number of days with the virus.
        """
        SimulationAgent.update_infected_agents(self)

    def update_vaccinated_agents_env(self) -> None:
        """Updates the vaccination status
        """
        SimulationAgent.update_vaccinated_agents(self)

    def __str__(self) -> str:
        """Overrides how the agent is printed.

        Returns:
            (String): Formatted string to print the agent.
        """
        return (f"\n\nAgent {self.unique_id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}"
                f"\nImmune System Response: {self.immune_system_response}\nPosition: {self.pos}\nInfected Days: {self.infected_days}")

    def __eq__(self, other) -> bool:
        """Overrides how the `==` operator is used in the SimulationAgent class.

        Returns:
            (Boolean): if agents' IDs are equal.
        """
        return self.unique_id == other.unique_id

    def __ne__(self, other) -> bool:
        """Overrides how the `!=` operator is used in the SimulationAgent class.

        Returns:
            (Boolean): if agents' IDs are different.
        """
        return self.unique_id != other.unique_id

    @staticmethod
    def update_vaccinated_agents(agent) -> None:
        if agent.vaccinated and agent.immune_system_response != constants.IMR_IMMUNE:
            # first dose
            if agent.vaccinated > constants.FIRST_DOSE_IMMUNE_TIME  \
                    and agent.immune_system_response != constants.IMR_ASYMPTOMATIC:

                prob = agent.model.random.random()
                if prob <= constants.FIRST_DOSE_IMMUNE_PRCNT:
                    new_imr = agent.random.randint(
                        constants.IMR_IMMUNE, constants.IMR_MODERATELY_INFECTED)  # can become immune or get a better response to the virus

                    if agent.immune_system_response > new_imr:  # only gets a better IMR
                        agent.immune_system_response = new_imr
                        logger.debug(
                            f'Agent {agent.unique_id} is now {constants.IMR_DICT[agent.immune_system_response]} after the first vaccine dose!')
            # second dose
            if agent.vaccinated > constants.SECOND_DOSE_IMMUNE_TIME and agent.vaccinated < constants.SECOND_DOSE_IMMUNE_TIME + 5 \
                    and agent.immune_system_response != constants.IMR_IMMUNE:  # 5 days of interval to get immune

                prob = agent.model.random.random()
                if prob <= constants.SECOND_DOSE_IMMUNE_PRCNT:
                    agent.immune_system_response = constants.IMR_IMMUNE  # got immune
                    logger.info(
                        f'Agent {agent.unique_id} is now IMR_IMMUNE after the second vaccine dose!')

            agent.vaccinated += 1

    @staticmethod
    def update_infected_agents(agent) -> None:
        """Updates the agents health status based on the number of days with the virus.

        This method can be called through the SimulationAgent class so we can update the agents in the quarantine room that are not in the simulation model grid.

        Args:
            agent (SimulationAgent): A SimulationAgent.
        """
        # evaluating time passing by, for all agents
        if (agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC) and not agent.recovered:
            # initializing value
            if agent.infected_days is None:
                agent.infected_days = 0
                agent.model.daily_infected += 1
                logger.debug(
                    f"Agent {agent.unique_id} is now on is day 0 for infected people. He is known as {agent.name}")

            # infected threshould where people recover
            elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED:
                value = random.random()
                # previous here is because people change to asymptomatic
                if agent.health_status == constants.SICK or agent.previous_health_status == constants.SICK:
                    if value < constants.RECOVERY_SEQUELS_P:
                        agent.health_status = constants.WITH_DISEASES_SEQUELAES
                        logger.debug(
                            f"Agent {agent.unique_id} recovered with sequels from being SICK. He is known as {agent.name}")
                    else:
                        agent.health_status = constants.TOTAL_RECOVERY
                        logger.debug(
                            f"Agent {agent.unique_id} recovered totaly from being SICK. He is known as {agent.name}")
                else:
                    agent.health_status = constants.TOTAL_RECOVERY
                    logger.debug(
                        f"Agent {agent.unique_id} recovered totaly. He is known as {agent.name}")
                agent.recovered = True
                agent.model.daily_recovered += 1
                # if agent recovers the Immune system is updated and upgraded
                agent.immune_system_response = agent.random.choice(
                    [constants.IMR_IMMUNE, constants.IMR_ASYMPTOMATIC])

            # case of deadly infected
            elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD:
                if agent.immune_system_response == constants.IMR_DEADLY_INFECTED:
                    agent.health_status = constants.DEAD
                    agent.model.daily_dead += 1
                    logger.debug(
                        f"Sadly Agent {agent.unique_id} died. He was known as {agent.name}")
                agent.infected_days += 1

            # infected threshould where people stop being contagious
            elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS:
                if agent.health_status != constants.ASYMPTOMATIC:
                    agent.previous_health_status = constants.SICK
                    agent.health_status = constants.ASYMPTOMATIC
                    logger.debug(
                        f"Agent {agent.unique_id} is now better and ASYMPTOMATIC. He is known as {agent.name}")

                agent.infected_days += 1
            else:
                agent.infected_days += 1

    @staticmethod
    def immune_response_by_age(age, health_status) -> int:
        """Returns the immune system response type according to the agent's age.

        Args:
            age (Integer): Agent's age.
            health_status (Integer): Agent's health status.

        Returns:
            (Integer): Immune system response type.
        """

        def age_probabilities(value, pdir, health_status) -> int:
            """Returns Immune response type based on age, health status, and probability of having a deadly immune system response.

            0______|P_DIR|_______1

            0__|ADM_HOSP_P|____|ADM_HOSP_P + ADM_HOSP_ICU_P|___|19/20|___|1/20|__1

            Args:
                value (Float): Random value between 0 and 1.
                pdir (Float): Probability of having a deadly immune system response based on the agent's age.
                health_status (INteger):Agent's health status.

            Returns:
                (Integer): Immune system response type.
            """
            value_d = random.random()
            if value < constants.ADM_HOSP_P:
                if value_d < pdir:
                    return constants.IMR_DEADLY_INFECTED
                else:
                    return constants.IMR_MODERATELY_INFECTED
            elif value > constants.ADM_HOSP_P and value < constants.ADM_HOSP_P + constants.ADM_HOSP_ICU_P:
                if value_d < pdir:
                    return constants.IMR_DEADLY_INFECTED
                else:
                    return constants.IMR_SEVERE_INFECTED
            else:  # prob of being healthy
                if value_d < pdir:
                    return constants.IMR_DEADLY_INFECTED
                elif value_d > pdir:
                    # 19.8/20 chances to be ASYMPTOMATIC over IMMUNE
                    if value < 19.8 * ((1-pdir) / 20):
                        return constants.IMR_ASYMPTOMATIC
                    else:
                        if health_status == constants.HEALTHY:  # only healthy people can be immune
                            return constants.IMR_IMMUNE
                        else:
                            return constants.IMR_ASYMPTOMATIC
        value = random.random()
        if age <= 9:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[0], health_status)
        elif age > 9 and age <= 19:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[1], health_status)
        elif age > 19 and age <= 29:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[2], health_status)
        elif age > 29 and age <= 39:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[3], health_status)
        elif age > 39 and age <= 49:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[4], health_status)
        elif age > 49 and age <= 59:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[5], health_status)
        elif age > 59 and age <= 69:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[6], health_status)
        elif age > 69 and age <= 79:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[7], health_status)
        elif age > 79:
            return age_probabilities(value, constants.AGE_P_DIR_ARRAY[8], health_status)

    @ staticmethod
    def value_based_probability(health_status, agent_immune_response, wear_mask_agent_in_contact, wear_mask_current_agent) -> int:
        """Returns the agent new health status based on its immune system type and on the health status of the agent in contact with.

        SICK_P| HEALTHY | ASSYMPTOMATIC_P|

        0____0.4 _________0.9___________________1

        Args:
            health_status (Integer): Health status of agent in contact with.
            agent_immune_response (Integer): Current agent imune response type.
            wear_mask_agent_in_contact (Boolean): If agent in contact wears a mask.
            wear_mask_current_agent (Boolean): If current agent wears a mask.

        Returns:
            Health Status (Integer): Agent new health status.
        """

        if health_status > constants.ASYMPTOMATIC or agent_immune_response == constants.IMR_IMMUNE:
            return -1  # do not change the agent's healthy status
        else:
            random_value = random.random()
            # using mask reduces the spread
            if wear_mask_agent_in_contact:
                mask_value = constants.CONTAGIOUS_AGENT_MASK
            elif wear_mask_agent_in_contact and wear_mask_current_agent:
                mask_value = constants.HEALTHY_AGENT_MASK
            elif wear_mask_current_agent:
                mask_value = constants.CONTAGIOUS_AGENT_MASK_HEALTHY_MASK
            else:
                mask_value = constants.CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK

            if random_value <= constants.SICK_P * mask_value:
                if agent_immune_response > constants.IMR_ASYMPTOMATIC:
                    return constants.SICK
                elif agent_immune_response == constants.IMR_ASYMPTOMATIC:
                    return constants.ASYMPTOMATIC
                elif agent_immune_response == constants.IMR_IMMUNE:
                    return -1

            elif random_value >= constants.SICK_P * mask_value and \
                    random_value <= constants.SICK_P * mask_value + constants.HEALTHY_P * mask_value:
                return constants.HEALTHY

            elif random_value >= 1 - constants.ASYMPTOMATIC_P * mask_value:
                if agent_immune_response > constants.IMR_ASYMPTOMATIC:
                    return constants.SICK
                elif agent_immune_response == constants.IMR_ASYMPTOMATIC:
                    return constants.ASYMPTOMATIC
                elif agent_immune_response == constants.IMR_IMMUNE:
                    return -1
            else:
                # when agents wear a mask, the probability count is less than 1 so we end up here, where the masks did not allow the contagious
                return -1
