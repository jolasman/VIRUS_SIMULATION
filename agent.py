from constants import IMR_DEADLY_INFECTED, IMR_MODERATELY_INFECTED, IMR_HIGHLY_INFECTED, IMR_ASYMPTOMATIC, IMR_IMMUNE, ADM_HOSP_P, \
    AGE_P_DIR_ARRAY, ADM_HOSP_ICU_P
import uuid
import random
from faker import Faker
fake = Faker()


class Agent:
    def __init__(self, pos_X, pos_Y, name="anonymous", age=None, health_status=0, immune_system_response=0):
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = fake.name()

        if health_status is None:
            health_status = 0

        if immune_system_response is None:
            immune_system_response = Agent.immune_response_by_age(age)

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

    def step(self, new_posX, new_posY):
        """
        Simulating the environment step
        """
        self.pos_X = new_posX
        self.pos_Y = new_posY

    def set_position(self, pos_X, pos_Y):
        """
        """
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.pos_tuple = (self.pos_X, self.pos_Y)

    def __str__(self):
        return f"\n\nAgent {self.id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}\nImmune System Response: {self.immune_system_response}\nPosition: ({self.pos_X}, {self.pos_Y}) "

    @staticmethod
    def immune_response_by_age(age):
        """
        Return the immune system response type according to the agent's age
        """
        def age_probabilities(value, pdir):
            """
            0______|P_DIR|_______1
            0__|ADM_HOSP_P|____|ADM_HOSP_P + ADM_HOSP_ICU_P|___|19/20|___|1/20|__1
            """
            value_d = random.random()
            if value < ADM_HOSP_P:
                if value_d < pdir:
                    return IMR_DEADLY_INFECTED
                else:
                    return IMR_MODERATELY_INFECTED
            elif value > ADM_HOSP_P and value < ADM_HOSP_P + ADM_HOSP_ICU_P:
                if value_d < pdir:
                    return IMR_DEADLY_INFECTED
                else:
                    return IMR_HIGHLY_INFECTED
            else:  # prob of being healthy
                if value_d < pdir:
                    return IMR_DEADLY_INFECTED
                elif value_d > pdir:
                # 19.8/20 chances to be ASYMPTOMATIC over IMMUNE
                    if value < 19.8 * ((1-pdir) / 20):
                        return IMR_ASYMPTOMATIC
                    else:
                        return IMR_IMMUNE

        value = random.random()
        if age <= 9:
            return age_probabilities(value, AGE_P_DIR_ARRAY[0])
        elif age > 9 and age <= 19:
            return age_probabilities(value, AGE_P_DIR_ARRAY[1])
        elif age > 19 and age <= 29:
            return age_probabilities(value, AGE_P_DIR_ARRAY[2])
        elif age > 29 and age <= 39:
            return age_probabilities(value, AGE_P_DIR_ARRAY[3])
        elif age > 39 and age <= 49:
            return age_probabilities(value, AGE_P_DIR_ARRAY[4])
        elif age > 49 and age <= 59:
            return age_probabilities(value, AGE_P_DIR_ARRAY[5])
        elif age > 59 and age <= 69:
            return age_probabilities(value, AGE_P_DIR_ARRAY[6])
        elif age > 69 and age <= 79:
            return age_probabilities(value, AGE_P_DIR_ARRAY[7])
        elif age > 79:
            return age_probabilities(value, AGE_P_DIR_ARRAY[8])
