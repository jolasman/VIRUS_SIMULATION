from agent import Agent
import random
from random import sample
from tqdm import tqdm
import sys
import math


from constants import SICK, SICK_P, ASYMPTOMATIC, ASYMPTOMATIC_P, HEALTHY, HEALTHY_P, TOTAL_RECOVERY, WITH_DISEASES_SEQUELAES, DEAD, IMR_IMMUNE, \
    SOCIAL_DISTANCE_STEP, INFECTED_DAYS_THRESHOLD_FOR_INFECTED, INFECTED_DAYS_THRESHOLD_FOR_DEAD, RECOVERY_SEQUELS_P, IMR_DEADLY_INFECTED, INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS, \
    CONTAGIOUS_DISTANCE, IMR_ASYMPTOMATIC


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

    def random_step_no_social_distance(self, random_limit, size,  p_of_agent_moving=1):
        """
        Simulating the environment step with no care about social distance
        """
        tuple_list = set()
        total = round(len(self.agent_list) * p_of_agent_moving)

        while len(tuple_list) < total:
            x = random.randint(1, size-1)
            y = random.randint(1, size-1)
            tuple_list.add((x, y))

        tuple_list = list(tuple_list)
        random.shuffle(tuple_list)

        for agent in random.sample(self.agent_list, total):
            (new_pos_X, new_pos_Y) = tuple_list.pop()
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

    def update_health_status(self):
        """
        Updates the status for each agent
        """
        for current_agent in self.agent_list:
            # creating a tupple list with the position and the health_status of each agent in the simulation
            tuple_list = [(agent_.pos_tuple, agent_.health_status)
                          for agent_ in self.agent_list]
            (x_0, y_0) = current_agent.pos_tuple  # get the agent position

            for ((x_1, y_1), hs_from_agent_in_contact) in tuple_list:  # for each agent in simulation
                # calculating the distance between the points
                dist = math.hypot(x_0 - x_1, y_0 - y_1)
                # if not the agent himself and ( it is not recoverd and inside the contagious range)
                if dist != 0 and (dist < CONTAGIOUS_DISTANCE and not current_agent.recovered):
                    # can get the virus, neverthless he got it once before, the recovered instance variable can change
                    if current_agent.health_status > ASYMPTOMATIC:
                        hs_new_value_for_current_agent = Simulation.value_based_probability(
                            hs_from_agent_in_contact, current_agent.immune_system_response)

                        if hs_new_value_for_current_agent != -1:
                            current_agent.health_status = hs_new_value_for_current_agent
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
