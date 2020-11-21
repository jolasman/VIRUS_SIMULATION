from agent import Agent
import random
from random import sample
from tqdm import tqdm
import sys

from constants import SICK, SICK_P, ASYMPTOMATIC, ASYMPTOMATIC_P, HEALTHY, HEALTHY_P, TOTAL_RECOVERY, WITH_DISEASES_SEQUELAES, DEAD

class Simulation:
    def __init__(self, name):
        self.name = name
        self.agent_list = []

    def random_step(self, random_limit, size,  p_of_agent_moving=1):
        """
        Simulating the environment step
        """
        total = round(len(self.agent_list) * p_of_agent_moving)
        for agent in random.sample(self.agent_list, total):
            new_pos_X = agent.pos_X + \
                random.randint(-random_limit, random_limit)
            new_pos_Y = agent.pos_Y + \
                random.randint(-random_limit, random_limit)
            tuple_list = [agent_.pos_tuple for agent_ in self.agent_list]
            while (new_pos_X, new_pos_Y) in tuple_list or \
                (new_pos_X <= 0 or new_pos_Y <= 0) or\
                    (new_pos_X >= size or new_pos_Y >= size):
                new_pos_X = agent.pos_X + \
                    random.randint(-random_limit, random_limit)
                new_pos_Y = agent.pos_Y + \
                    random.randint(-random_limit, random_limit)

            agent.set_position(new_pos_X, new_pos_Y)
            agent.set_health_status(self.agent_list)  # changing health status

    def create_agent(self, pos_X, pos_Y, name=None, age=None, health_status=None,
                     immune_system_response=None):
        """
        Getting the current state data to build charts
        """
        new_agent = Agent(pos_X, pos_Y, name=name, age=age, health_status=health_status,
                          immune_system_response=immune_system_response)
        self.agent_list.append(new_agent)

    def set_health_status_at_hospital(self):
        """
        """
        for agent in self.agent_list:
            # evaluating time passing by, for all agents
            if (agent.health_status == SICK or agent.health_status == ASYMPTOMATIC) and not agent.recovered:
                if agent.infected_days is None:
                    agent.infected_days = 0
                elif agent.infected_days == 10:
                    agent.health_status = WITH_DISEASES_SEQUELAES
                    agent.recovered = True
                else:
                    agent.infected_days += 1

    def get_all_agents(self):
        """
        Simulating the environment step
        """
        return self.agent_list

    def get_infected(self):
        """
        Getting the current state data to build charts
        """
        infected = [1 for x in self.agent_list if x.health_status ==
                    SICK or x.health_status == ASYMPTOMATIC]
        return sum(infected)

    def get_healed(self):
        """
        Getting the current state data to build charts
        """
        healed = [1 for x in self.agent_list if x.health_status ==
                  WITH_DISEASES_SEQUELAES or x.health_status == TOTAL_RECOVERY]
        return sum(healed)

    def get_dead(self):
        """
        Getting the current state data to build charts
        """
        dead = [1 for x in self.agent_list if x.health_status == DEAD]
        return sum(dead)

    def get_healthy(self):
        """
        Getting the current state data to build charts
        """
        healthy = [1 for x in self.agent_list if x.health_status == HEALTHY]
        return sum(healthy)
