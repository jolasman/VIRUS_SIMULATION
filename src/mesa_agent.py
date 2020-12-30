from mesa import Agent
import constants
import uuid
import random
from faker import Faker
fake = Faker()


class SimulationAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, model,  name="anonymous", age=None, health_status=None, immune_system_response=None, wear_mask=None):
        id_ = uuid.uuid1()
        super().__init__(id_, model)
        self.wealth = 1
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = fake.name()

        if health_status is None:
            health_status = random.randint(constants.SICK, constants.HEALTHY)

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
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

    def get_health_status(self):
        return self.health_status

    def __str__(self):
        """Overrides how the agent is printed

        Returns:
            (String): Formatted string to print the agent
        """
        return (f"\n\nAgent {self.unique_id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}"
                f"\nImmune System Response: {self.immune_system_response}\nPosition: ({self.pos})")

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
