from agent import Agent
import random
from random import sample
from tqdm import tqdm
import sys

from constants import SICK, SICK_P, ASYMPTOMATIC, ASYMPTOMATIC_P, HEALTHY, HEALTHY_P, TOTAL_RECOVERY, WITH_DISEASES_SEQUELAES, DEAD, IMR_IMMUNE, \
    SOCIAL_DISTANCE_STEP, INFECTED_DAYS_THRESHOLD_FOR_INFECTED, INFECTED_DAYS_THRESHOLD_FOR_DEAD, RECOVERY_SEQUELS_P, IMR_DEADLY_INFECTED, INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS


class Simulation:
    def __init__(self, name):
        self.name = name
        self.agent_list = []

    def update_health_status(self):
        """
        Updates the status for each agent
        """
        for agent in self.agent_list:
            agent.set_health_status(self.agent_list)  # changing health status

    def random_step(self, random_limit, size,  p_of_agent_moving=1):
        """
        Simulating the environment step
        """
        total = round(len(self.agent_list) * p_of_agent_moving)
        print(f"total: {total}")
        for agent in random.sample(self.agent_list, total):
            has_value = False

            new_pos_X = agent.pos_X + \
                random.randint(-random_limit, random_limit)

            new_pos_Y = agent.pos_Y + \
                random.randint(-random_limit, random_limit)

            tuple_list = [agent_.pos_tuple for agent_ in self.agent_list]

            while not has_value:
                can_add = True
                x_loop_must_break = False
                for x_ax in range(SOCIAL_DISTANCE_STEP + 1):
                    for y_ax in range(SOCIAL_DISTANCE_STEP + 1):
                        if (new_pos_X + x_ax, new_pos_Y + y_ax) in tuple_list or \
                            (new_pos_X + x_ax, new_pos_Y - y_ax) in tuple_list or \
                            (new_pos_X - x_ax, new_pos_Y + y_ax) in tuple_list or\
                                (new_pos_X - x_ax, new_pos_Y - y_ax) in tuple_list:
                            can_add = False
                            x_loop_must_break = True
                    if x_loop_must_break:
                        break

                if can_add and (new_pos_X >= size or new_pos_Y >= size or new_pos_X < 0 or new_pos_Y < 0):
                    can_add = False

                if not can_add:
                    new_pos_X = agent.pos_X + \
                        random.randint(-random_limit, random_limit)
                    new_pos_Y = agent.pos_Y + \
                        random.randint(-random_limit, random_limit)
                else:
                    has_value = True

            agent.set_position(new_pos_X, new_pos_Y)

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
                # initializing value
                if agent.infected_days is None:
                    agent.infected_days = 0

                # infected threshould where people recover
                elif agent.infected_days == INFECTED_DAYS_THRESHOLD_FOR_INFECTED:
                    value = random.random()
                    if agent.health_status == SICK or agent.previous_health_status == SICK:
                        if value < RECOVERY_SEQUELS_P:
                            agent.health_status = WITH_DISEASES_SEQUELAES
                        else:
                            agent.health_status = TOTAL_RECOVERY
                    else:
                        agent.health_status = TOTAL_RECOVERY
                    agent.recovered = True

                # case of deadly infected
                elif agent.infected_days == INFECTED_DAYS_THRESHOLD_FOR_DEAD:
                    if agent.immune_system_response == IMR_DEADLY_INFECTED:
                        agent.health_status = DEAD
                        # the agent actually did not recovered bu we avoid iterations using the first if condition
                        agent.recovered = True
                    agent.infected_days += 1

                # infected threshould where people stop being contagious
                elif agent.infected_days == INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS:
                    if agent.health_status != ASYMPTOMATIC:
                        agent.previous_health_status = SICK
                        agent.health_status = ASYMPTOMATIC

                    agent.infected_days += 1
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
        return len([x for x in self.agent_list if x.health_status ==
                    SICK or x.health_status == ASYMPTOMATIC])

    def get_healed(self):
        """
        Getting the current state data to build charts
        """
        return len([x for x in self.agent_list if x.health_status ==
                    WITH_DISEASES_SEQUELAES or x.health_status == TOTAL_RECOVERY])

    def get_dead(self):
        """
        Getting the current state data to build charts
        """
        return len([x for x in self.agent_list if x.health_status == DEAD])

    def get_healthy(self):
        """
        Getting the current state data to build charts
        """
        return len([x for x in self.agent_list if x.health_status == HEALTHY])

    def get_immune_people(self):
        """
        Getting the current state data to build charts
        """
        return len([x for x in self.agent_list if x.immune_system_response == IMR_IMMUNE])
