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


class SimulationAgent(Agent):
    """Class representing a human being
    """

    def __init__(self, model,  name=None, age=None, health_status=None, immune_system_response=None, wear_mask=None):
        """Class constructor

        Args:
            model (Mesa Model): The simulations model
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
            health_status = random.choice([constants.SICK, constants.HEALTHY])

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

    def move(self):
        """[summary]
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def agents_in_contact(self):
        """[summary]
        """
        cellmates = self.model.grid.get_cell_list_contents(
            [self.pos])  # find others in the same cell
        if len(cellmates) > 1:
            for agent in cellmates:
                # excluding the day 0, when the agents get the infection, where we change from None to 0
                if agent.infected_days and not self.recovered:
                    # can get the virus, neverthless he got it once before, the recovered instance variable can change
                    if self.health_status > constants.ASYMPTOMATIC:
                        hs_new_value_for_current_agent = SimulationAgent.value_based_probability(
                            agent.health_status, self.immune_system_response, agent.wear_mask, self.wear_mask)
                        if hs_new_value_for_current_agent != -1:
                            self.health_status = hs_new_value_for_current_agent
                            #self.daily_infected += 1
                            logger.debug(
                                f"Agent {self.unique_id} had an update in his health status: {constants.HEALTH_STATUS_DICT[self.health_status]}")

    def step(self):
        """[summary]
        """
        self.move()
        self.agents_in_contact()
        self.update_infected_agents()

    def get_health_status(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.health_status

    def update_infected_agents(self):
        """Updates the agents health status based on the number of days infected with the virus
        """
        # evaluating time passing by, for all agents
        if (self.health_status == constants.SICK or self.health_status == constants.ASYMPTOMATIC) and not self.recovered:
            # initializing value
            if self.infected_days is None:
                self.infected_days = 0
                logger.debug(
                    f"Agent {self.unique_id} is now on is day 0 for infected people. He is known as {self.name}")

            # infected threshould where people recover
            elif self.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED:
                value = random.random()
                # previous here is because people change to asymptomatic
                if self.health_status == constants.SICK or self.previous_health_status == constants.SICK:
                    if value < constants.RECOVERY_SEQUELS_P:
                        self.health_status = constants.WITH_DISEASES_SEQUELAES
                        logger.debug(
                            f"Agent {self.unique_id} recovered with sequels from being SICK. He is known as {self.name}")
                    else:
                        self.health_status = constants.TOTAL_RECOVERY
                        logger.debug(
                            f"Agent {self.unique_id} recovered totaly from being SICK. He is known as {self.name}")
                else:
                    self.health_status = constants.TOTAL_RECOVERY
                    logger.debug(
                        f"Agent {self.unique_id} recovered totaly. He is known as {self.name}")
                self.recovered = True
                #self.daily_healed += 1

            # case of deadly infected
            elif self.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD:
                if self.immune_system_response == constants.IMR_DEADLY_INFECTED:
                    self.health_status = constants.DEAD
                    #self.daily_dead += 1
                    # if self.pos_tuple == (constants.QUARANTINE_X, constants.QUARANTINE_Y):
                    #self.daily_quarantine -= 1

                    logger.debug(
                        f"Sadly Agent {self.unique_id} died. He was known as {self.name}")
                self.infected_days += 1

            # infected threshould where people stop being contagious
            elif self.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS:
                if self.health_status != constants.ASYMPTOMATIC:
                    self.previous_health_status = constants.SICK
                    self.health_status = constants.ASYMPTOMATIC
                    logger.debug(
                        f"Agent {self.unique_id} is now better and ASYMPTOMATIC. He is known as {self.name}")

                self.infected_days += 1
            else:
                self.infected_days += 1

    def __str__(self):
        """Overrides how the agent is printed

        Returns:
            (String): Formatted string to print the agent
        """
        return (f"\n\nAgent {self.unique_id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}"
                f"\nImmune System Response: {self.immune_system_response}\nPosition: {self.pos}\nInfected Days: {self.infected_days}")

    @staticmethod
    def immune_response_by_age(age, health_status):
        """Returns the immune system response type according to the agent's age

        Args:
            age (Integer): Agent's age
            health_status (Integer): Agent's health status

        Returns:
            (Integer): Immune system response type
        """

        def age_probabilities(value, pdir, health_status):
            """Returns Immune response type based on age, health status, and probability of having a deadly immune system response

            0______|P_DIR|_______1

            0__|ADM_HOSP_P|____|ADM_HOSP_P + ADM_HOSP_ICU_P|___|19/20|___|1/20|__1

            Args:
                value (Float): Random value between 0 and 1
                pdir (Float): Probability of having a deadly immune system response based on the agent's age
                health_status (INteger):Agent's health status

            Returns:
                (Integer): Immune system response type
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
                    return constants.IMR_HIGHLY_INFECTED
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
    def value_based_probability(health_status, agent_immune_response, wear_mask_agent_in_contact, wear_mask_current_agent):
        """Returns the agent new health status based on its immune system type and on the health status of the agent in contact with

        SICK_P| HEALTHY | ASSYMPTOMATIC_P|

        0____0.4 _________0.9___________________1

        Args:
            health_status (Integer): Health status of agent in contact with
            agent_immune_response (Integer): Current agent imune response type
            wear_mask_agent_in_contact (Boolean): If agent in contact wears a mask
            wear_mask_current_agent (Boolean): If current agent wears a mask

        Returns:
            Health Status (Integer): Agent new health status
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
