import constants
import uuid
import random
from faker import Faker
fake = Faker()


class Agent:
    """Class representing a human being
    """
    def __init__(self, pos_X, pos_Y, name="anonymous", age=None, health_status=0, immune_system_response=0, wear_mask=None):
        """Class constructor

        Args:
            pos_X (Integer): Agent's x axis position
            pos_Y (Integer): Agent's y axis position
            name (str, optional): Agent's name. Defaults to "anonymous".
            age (Integer, optional): Agent's age. Defaults to None.
            health_status (inIntegert, optional): Agent's health status. Defaults to 0.
            immune_system_response (Integer, optional): Agent's Immune System response type. Defaults to 0.
            wear_mask (Boolean, optional): If agent wears a mask. Defaults to None.
        """
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = fake.name()

        if health_status is None:
            health_status = 0

        if immune_system_response is None:
            immune_system_response = Agent.immune_response_by_age(age, health_status)

        if wear_mask is None:
            wear_mask = bool(random.getrandbits(1))

        self.id = uuid.uuid1()
        self.name = name
        self.age = age
        self.health_status = health_status
        self.previous_health_status = None
        self.immune_system_response = immune_system_response
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.pos_tuple = (self.pos_X, self.pos_Y)
        self.infected_days = None
        self.recovered = False
        self.wear_mask = wear_mask
        self.quarantine = False


    def set_position(self, pos_X, pos_Y):
        """Changes the agent's position to a new one

        Args:
            new_posX (Integer): x axis position
            new_posY (Integer): y axis position
        """
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.pos_tuple = (self.pos_X, self.pos_Y)

    def __str__(self):
        """Overrides how the agent is printed

        Returns:
            (String): Formatted string to print the agent
        """
        return f"\n\nAgent {self.id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}\nImmune System Response: {self.immune_system_response}\nPosition: ({self.pos_X}, {self.pos_Y}) "

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
                        if health_status == constants.HEALTHY: # only healthy people can be immune
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
