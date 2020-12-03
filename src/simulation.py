import constants
from agent import Agent
import random
from random import sample
from tqdm import tqdm
import sys
import math
import logging

logging.basicConfig(
    level=constants.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)


class Simulation:
    """Class representing the simulation
    """
    def __init__(self, name):
        """Simulation constructor

        Args:
            name (Any): Simulation's name
        """
        self.name = name
        self.agent_list = []
        self.daily_infected = 0
        self.daily_healed = 0
        self.daily_dead = 0
        self.daily_quarantine = 0

    def random_step(self, random_limit, size,  p_of_agent_moving=1):
        """Simulating the environment step

        Args:
            random_limit (Integer): Maximum number of units on each axis that each agent can move
                        size (Integer): Environment size
            p_of_agent_moving (Float, optional): Percentage of agents that move in the step. Defaults to 1.
        """
        total = round(len(self.agent_list) * p_of_agent_moving)
        for agent in random.sample(self.agent_list, total):
            if agent.health_status != constants.DEAD and agent.pos_tuple != (constants.QUARANTINE_X, constants.QUARANTINE_Y):
                has_value = False

                new_pos_X = agent.pos_X + \
                    random.randint(-random_limit, random_limit)

                new_pos_Y = agent.pos_Y + \
                    random.randint(-random_limit, random_limit)

                tuple_list = [agent_.pos_tuple for agent_ in self.agent_list]

                while not has_value:
                    can_add = True
                    x_loop_must_break = False
                    for x_ax in range(constants.SOCIAL_DISTANCE_STEP + 1):
                        for y_ax in range(constants.SOCIAL_DISTANCE_STEP + 1):
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
                logging.debug(
                    f"Agent {agent.id} moved to a new position: {agent.pos_tuple}")
            elif agent.health_status == constants.DEAD:
                if agent.pos_tuple != (constants.DEAD_X, constants.DEAD_Y):
                    agent.set_position(constants.DEAD_X, constants.DEAD_Y)

    def random_step_no_social_distance(self, size,  p_of_agent_moving=1):
        """Simulating the environment step with no care about social distance

        Args:
            size (Integer): Environment size
            p_of_agent_moving (Float, optional): Percentage of agents that move in the step. Defaults to 1.
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
            # Dead people do not move # quarantine people stay there
            if agent.health_status != constants.DEAD and agent.pos_tuple != (constants.QUARANTINE_X, constants.QUARANTINE_Y):
                (new_pos_X, new_pos_Y) = tuple_list.pop()
                agent.set_position(new_pos_X, new_pos_Y)
                logging.debug(
                    f"Agent {agent.id} moved to a new position: {agent.pos_tuple}. He does not care about social distance!")
            elif agent.health_status == constants.DEAD:
                if agent.pos_tuple != (constants.DEAD_X, constants.DEAD_Y):
                    agent.set_position(constants.DEAD_X, constants.DEAD_Y)

    def create_agent(self, pos_X, pos_Y, name=None, age=None, health_status=None,
                     immune_system_response=None, wear_mask=None):
        """Create a new agent for the Simulation instance

        Args:
            pos_X (Integer): X axis position
            pos_Y (Integer): Y axis position
            name (String, optional): Agent's name. Defaults to None.
            age (Integer, optional): Agent's age. Defaults to None.
            health_status (Integer, optional): Agent's health status. Defaults to None.
            immune_system_response (Integer, optional): Agent's immune response system type. Defaults to None.
        """
        new_agent = Agent(pos_X, pos_Y, name=name, age=age, health_status=health_status,
                          immune_system_response=immune_system_response, wear_mask=wear_mask)
        self.agent_list.append(new_agent)

    def set_health_status_by_day(self):
        """Updates the agents health status based on the number of days infected with the virus
        """
        for agent in self.agent_list:
            # evaluating time passing by, for all agents
            if (agent.health_status == constants.SICK or agent.health_status == constants.ASYMPTOMATIC) and not agent.recovered:
                # initializing value
                if agent.infected_days is None:
                    agent.infected_days = 0
                    logging.debug(
                        f"Agent {agent.id} is now on is day 0 for infected people. He is known as {agent.name}")

                # infected threshould where people recover
                elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED:
                    value = random.random()
                    # previous here is because people change to asymptomatic
                    if agent.health_status == constants.SICK or agent.previous_health_status == constants.SICK:
                        if value < constants.RECOVERY_SEQUELS_P:
                            agent.health_status = constants.WITH_DISEASES_SEQUELAES
                            logging.debug(
                                f"Agent {agent.id} recovered with sequels from being SICK. He is known as {agent.name}")
                        else:
                            agent.health_status = constants.TOTAL_RECOVERY
                            logging.debug(
                                f"Agent {agent.id} recovered totaly from being SICK. He is known as {agent.name}")
                    else:
                        agent.health_status = constants.TOTAL_RECOVERY
                        logging.debug(
                            f"Agent {agent.id} recovered totaly. He is known as {agent.name}")
                    agent.recovered = True
                    self.daily_healed += 1

                # case of deadly infected
                elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD:
                    if agent.immune_system_response == constants.IMR_DEADLY_INFECTED:
                        agent.health_status = constants.DEAD
                        self.daily_dead += 1
                        if agent.pos_tuple == (constants.QUARANTINE_X, constants.QUARANTINE_Y):
                            self.daily_quarantine -= 1

                        logging.debug(
                            f"Sadly Agent {agent.id} died. He was known as {agent.name}")
                    agent.infected_days += 1

                # infected threshould where people stop being contagious
                elif agent.infected_days == constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS:
                    if agent.health_status != constants.ASYMPTOMATIC:
                        agent.previous_health_status = constants.SICK
                        agent.health_status = constants.ASYMPTOMATIC
                        logging.debug(
                            f"Agent {agent.id} is now better and ASYMPTOMATIC. He is known as {agent.name}")

                    agent.infected_days += 1
                else:
                    agent.infected_days += 1

    def update_health_status(self):
        """
        Updates the status for each agent when in contact with other agents
        """
        for current_agent in self.agent_list:
            # creating a tupple list with the position, the health_status, and the infected days of each agent in the simulation
            tuple_list = [(agent_.pos_tuple, agent_.health_status, agent_.infected_days, agent_.wear_mask)
                          for agent_ in self.agent_list]
            (x_0, y_0) = current_agent.pos_tuple  # get the agent position

            # for each agent in simulation
            for ((x_1, y_1), hs_from_agent_in_contact, inf_day_agent_in_contact, wear_mask_agent_in_contact) in tuple_list:
                # calculating the distance between the points
                dist = math.hypot(x_0 - x_1, y_0 - y_1)
                # if not the agent himself and ( it is not recoverd and inside the contagious range) and (agent in contact is sick)
                if dist != 0 and (dist < constants.CONTAGIOUS_DISTANCE and not current_agent.recovered) and hs_from_agent_in_contact < constants.WITH_DISEASES_SEQUELAES:
                    if inf_day_agent_in_contact:  # excluding the day 0, when the agents get the infection, where we change from None to 0
                        # can get the virus, neverthless he got it once before, the recovered instance variable can change
                        if current_agent.health_status > constants.ASYMPTOMATIC:
                            hs_new_value_for_current_agent = Simulation.value_based_probability(
                                hs_from_agent_in_contact, current_agent.immune_system_response, wear_mask_agent_in_contact, current_agent.wear_mask)

                            if hs_new_value_for_current_agent != -1:
                                current_agent.health_status = hs_new_value_for_current_agent
                                self.daily_infected += 1
                                logging.debug(
                                    f"Agent {current_agent.id} had an update in his health status: {constants.HEALTH_STATUS_DICT[current_agent.health_status]}")
                                break

    def update_quarantine(self, size):
        """Updates the status for each agent in quarantine

        Args:

            size (Integer): Environment size
        """
        for agent in self.get_infected()[:int(len(self.get_infected()) * constants.QUARANTINE_PERCENTAGE)]:  # only half agents go to quarantine, the others remain indetected by autorities
            # quarantine zone
            agent.set_position(constants.QUARANTINE_X, constants.QUARANTINE_Y)
            agent.quarantine = True
            self.daily_quarantine += 1
            logging.debug(f"Agent {agent.id} is now in quarantine. ")

        # removing healed people from quarantine
        for agent in self.agent_list:
            if agent.health_status > constants.ASYMPTOMATIC and agent.pos_tuple == (constants.QUARANTINE_X, constants.QUARANTINE_Y):
                if constants.SOCIAL_DISTANCE_STEP == 0:
                    tuple_set = set(
                        [agent.pos_tuple for agent in self.agent_list])
                    total = len(self.agent_list)

                    while len(tuple_set) < total + 1:
                        x = random.randint(1, size-1)
                        y = random.randint(1, size-1)
                        tuple_set.add((x, y))

                    list_ = list(tuple_set)
                    (pos_X, pos_Y) = list_.pop()
                    agent.set_position(pos_X, pos_Y)
                    self.daily_quarantine -= 1
                    logging.debug(
                        f"Agent {agent.id} returns to the environment at {agent.pos_tuple}")

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

        if health_status > 1 or agent_immune_response == constants.IMR_IMMUNE:
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

    def get_all_agents(self):
        """Returns the list of agents for the Simulation instance

        Returns:
            agent_list (List): List of agents
        """
        return self.agent_list

    def get_quarantine_count(self):
        """Number of agents in quarantine

        Returns:
            (Integer): Number of agents
        """
        return len([agent for agent in self.agent_list
                    if agent.pos_tuple == (constants.QUARANTINE_X, constants.QUARANTINE_Y)])

    def get_infected_count(self):
        """Number of agents infected

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if (x.health_status ==
                                                   constants.SICK or x.health_status == constants.ASYMPTOMATIC)])

    def get_infected(self):
        """List of infected agents not in quarantine

        Returns:
            (List): Infected agents
        """
        return [x for x in self.agent_list if x.pos_tuple != (constants.QUARANTINE_X, constants.QUARANTINE_Y) and
                (x.health_status ==
                 constants.SICK or x.health_status == constants.ASYMPTOMATIC)]

    def get_healed_count(self):
        """Number of healead agents

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.health_status ==
                    constants.WITH_DISEASES_SEQUELAES or x.health_status == constants.TOTAL_RECOVERY])

    def get_healed_quarantine_count(self):
        """Number of healead agents that was on quarantine

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.quarantine and
                    (x.health_status == constants.WITH_DISEASES_SEQUELAES or x.health_status == constants.TOTAL_RECOVERY)])

    def get_dead_count(self):
        """Number of dead agents

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.health_status == constants.DEAD])

    def get_dead_quarantine_count(self):
        """Number of dead agents from quarantine

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.quarantine and x.health_status == constants.DEAD])

    def get_healthy_count(self):
        """Number of healthy agents

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.health_status == constants.HEALTHY])

    def get_immune_people_count(self):
        """Number of immune agents

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.immune_system_response == constants.IMR_IMMUNE])

    def get_wearing_mask_count(self):
        """Number of agents wearing mask

        Returns:
            (Integer): Number of agents
        """
        return len([x for x in self.agent_list if x.wear_mask])

    def reset_daily_data(self):
        """Resets the daily total to "0"

        """
        self.daily_infected = 0
        self.daily_healed = 0
        self.daily_dead = 0
        self.daily_quarantine = 0

    def get_daily_data(self):
        """Returns daily data counters. You should call the reset_daily_data class method after using this one

        Returns:
            self.daily_infected (Integer), self.daily_healed (Integer), self.daily_dead (Integer), self.daily_quarantine (Integer): daily counters
        """
        return self.daily_infected, self.daily_healed, self.daily_dead, self.daily_quarantine
