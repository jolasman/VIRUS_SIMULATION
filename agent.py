
import uuid
import random
import math

from constants import SICK, SICK_P, ASYMPTOMATIC, ASYMPTOMATIC_P, HEALTHY, HEALTHY_P, IMR_IMMUNE, IMR_ASYMPTOMATIC, IMR_MODERATELY_INFECTED, \
    IMR_HIGHLY_INFECTED, CONTAGIOUS_DISTANCE, HEALTH_STATUS_DICT


class Agent:
    def __init__(self, pos_X, pos_Y, name="anonymous", age=None, health_status=0, immune_system_response=0):
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = "anonymous"

        if health_status is None:
            health_status = 0

        if immune_system_response is None:
            immune_system_response = 0

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

    def set_health_status(self, agents_list):
        """
        """
        for agent in agents_list:
            if agent.id != self.id:
                # if agents distance is less than contagious distance metters
                if math.hypot(agent.pos_X - self.pos_X, agent.pos_Y - self.pos_Y) < CONTAGIOUS_DISTANCE and not self.recovered:
                    if self.health_status > 1:  # can get the virus
                        health_status_new_value = Agent.value_based_probability(
                            agent.health_status, self.immune_system_response)

                        if health_status_new_value != -1:
                            if agent.health_status == SICK:
                                self.health_status = health_status_new_value
                                break
                            elif agent.health_status == ASYMPTOMATIC:
                                self.health_status = health_status_new_value
                                break

    @staticmethod
    def value_based_probability(health_status, agent_immune_response):
        """
        SICK_P| HEALTHY | ASSYMPTOMATIC_P|
        0____0.4 _____0.9________________1
        """
        if health_status > 1 or agent_immune_response == IMR_IMMUNE:
            return -1  # do not change the agent's healthy status
        else:
            random_value = random.random()
            if random_value <= SICK_P:
                if agent_immune_response > IMR_ASYMPTOMATIC:
                    return SICK
                elif agent_immune_response == IMR_ASYMPTOMATIC:
                    return ASYMPTOMATIC
                elif agent_immune_response == IMR_IMMUNE:
                    return -1

            elif random_value >= SICK_P and random_value <= SICK_P + HEALTHY_P:
                return HEALTHY

            elif random_value >= 1 - ASYMPTOMATIC_P:
                if agent_immune_response > IMR_ASYMPTOMATIC:
                    return SICK
                elif agent_immune_response == IMR_ASYMPTOMATIC:
                    return ASYMPTOMATIC
                elif agent_immune_response == IMR_IMMUNE:
                    return -1

    def __str__(self):
        return f"\n\nAgent {self.id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}\nImmune System Response: {self.immune_system_response}\nPosition: ({self.pos_X}, {self.pos_Y}) "
