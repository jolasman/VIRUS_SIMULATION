__author__ = "Joel Carneiro"
__copyright__ = "Copyright 2020, Open Source Project"
__credits__ = ["Joel Carneiro"]
__license__ = "Apache License 2.0"
__version__ = "1.0"
__maintainer__ = "Joel Carneiro"
__email__ = "jolasman@hotmail.com"
__status__ = "Development"

from simulation import Simulation
import random

import time
import logging
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image  # for creating visual of our env
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from matplotlib.ticker import MaxNLocator
import constants

logging.basicConfig(
    level=constants.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)

# TODO
# After n days people can get the virus again
# Adding a vaccine
# add mask
# washing hands


def static_simulation(sick_nbr, immmune_imr_nbr, asymp_imr_nbr, mod_imr_nbr, high_imr_nbr, dead_imr_nbr):
    """ Defining number of people for sick healthy and immune people

    Args:
        * sick_nbr (Integer): number of sick people
        * immmune_imr_nbr (Integer): number of people with immune resposnse system as IMR_IMMUNE
        * asymp_imr_nbr (Integer): number of with immune resposnse system as IMR_ASYMPTOMATIC
        * mod_imr_nbr (Integer): number of with immune resposnse system as IMR_MODERATELY_INFECTED
        * high_imr_nbr (Integer): number of with immune resposnse system as IMR_HIGHLY_INFECTED
        * dead_imr_nbr (Integer): number of with immune resposnse system as IMR_DEADLY_INFECTED

    Returns:
       hs_array (List), imr_array (List): The two arrays with the data to use
    """

    sick_array = [constants.SICK for x in range(sick_nbr)]
    healthy_array = [constants.HEALTHY for x in range(constants.TOTAL_NUMBER_OF_AGENTS - sick_nbr)]
    hs_array = sick_array + healthy_array
    random.shuffle(hs_array)

    immune_array = [constants.IMR_IMMUNE for x in range(immmune_imr_nbr)]
    asymp_array = [constants.IMR_ASYMPTOMATIC for x in range(asymp_imr_nbr)]
    mod_array = [constants.IMR_MODERATELY_INFECTED for x in range(mod_imr_nbr)]
    high_array = [constants.IMR_HIGHLY_INFECTED for x in range(high_imr_nbr)]
    dead_array = [constants.IMR_DEADLY_INFECTED for x in range(dead_imr_nbr)]

    imr_array = immune_array + asymp_array + mod_array + high_array + dead_array
    random.shuffle(imr_array)

    return hs_array, imr_array


def generate_random_tuple_list():
    """Builds a list with unique values of X and Y coordinates as tuples

    Returns:
        tuple_list (Tuple): Tuple of runique random positions
    """
    tuple_list = set()
    while len(tuple_list) < constants.TOTAL_NUMBER_OF_AGENTS:
        x = random.randint(0 + constants.RANDOM_LIMIT, constants.SIZE-constants.RANDOM_LIMIT)
        y = random.randint(0 + constants.RANDOM_LIMIT, constants.SIZE-constants.RANDOM_LIMIT)
        tuple_list.add((x, y))

    tuple_list = list(tuple_list)
    random.shuffle(tuple_list)

    return tuple_list


def get_random_pos(random_tuple_list):
    """Returns the last tuple as x and y variables for the given list of tuples

    Args:
        random_tuple_list ([type]): [description]

    Returns:
        pos_X (Integer), pos_Y (Integer): Two variable with the X and Y positions to use
    """
    (new_pos_X, new_pos_Y) = random_tuple_list.pop()
    return new_pos_X, new_pos_Y


def available_random_pos(simulation):
    """Returns unique x and y variables based on social distance constant.

    Args:
        simulation (Simulation): Instance of Simulation class

    Returns:
        pos_X (Integer), pos_Y (Integer): Two variable with the X and Y positions to use
    """
    new_pos_X = 0
    new_pos_Y = 0
    has_value = False
    for _ in simulation.agent_list:
        new_pos_X = random.randint(0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
        new_pos_Y = random.randint(0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
        tuple_list = [
            agent_.pos_tuple for agent_ in simulation.agent_list]
        while not has_value:
            can_add = True
            x_loop_must_break = False
            for x_ax in range(constants.SOCIAL_DISTANCE + 1):
                for y_ax in range(constants.SOCIAL_DISTANCE + 1):
                    if (new_pos_X + x_ax, new_pos_Y + y_ax) in tuple_list or \
                        (new_pos_X + x_ax, new_pos_Y - y_ax) in tuple_list or \
                        (new_pos_X - x_ax, new_pos_Y + y_ax) in tuple_list or\
                            (new_pos_X - x_ax, new_pos_Y - y_ax) in tuple_list:
                        can_add = False
                        x_loop_must_break = True
                if x_loop_must_break:
                    break

            if can_add and (new_pos_X >= constants.SIZE or new_pos_Y >= constants.SIZE):
                can_add = False

            if not can_add:
                new_pos_X = random.randint(
                    0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
                new_pos_Y = random.randint(
                    0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
            else:
                has_value = True

    return new_pos_X, new_pos_Y


def show_graphic_simulation(simulation):
    """Builds an image to represent the environment graphically and displays it

    Args:
        simulation (Simulation): Instance of Simulation class
    """
    # starts an rbg of our size
    env = np.zeros((constants.SIZE, constants.SIZE, 3), dtype=np.uint8)
    for agent in simulation.agent_list:
        # agents with negative coords are dead or in quarentine
        if agent.pos_tuple > (0, 0):
            env[agent.pos_X][agent.pos_Y] = constants.COLORS_DICT[agent.health_status]

    # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = Image.fromarray(env, 'RGB')
    # resizing so we can see our agent in all its glory.
    img = img.resize((constants.SIMULATION_GRAPHICS_SIZE_X, constants.SIMULATION_GRAPHICS_SIZE_Y))

    cv2.imshow("image", np.array(img))
    cv2.waitKey(200)


def show_detailed_data(infected, healed, healthy, dead, simulation):
    """
    """
    pass


def create_simulation_agents(new_simulation, random_tuple_list, hs_data=None, imr_data=None):
    """Adds all agents to the simulation

    Args:
        new_simulation (Simulation): Simulation instance
        random_tuple_list (Tuple): Tuple with generated positions for each agent
        hs_data (list, optional): List with health data status for each agent. Defaults to None.
        imr_data (list, optional): List with immune system response data for each agent. Defaults to None.
    """
    if constants.SOCIAL_DISTANCE == 0:
        new_pos_X, new_pos_Y = get_random_pos(random_tuple_list)
    else:
        new_pos_X, new_pos_Y = available_random_pos(new_simulation)

    if hs_data is None:
        health_value = np.random.choice(
            constants.HEALTH_ARRAY, p=constants.HEALTH_ARRAY_P, size=(1))[0]
    else:
        health_value = hs_data.pop()

    if imr_data is None:
        immune_response_value = None
    else:
        immune_response_value = imr_data.pop()

    new_simulation.create_agent(
        new_pos_X, new_pos_Y, health_status=health_value, immune_system_response=immune_response_value)


def main(random_simulation, graphics_simulation, static_beginning):
    """Runs the simulation

    Args:
        random_simulation (Boolean): If simulation agent's movement is random based
        graphics_simulation (Boolean): If show the environment graphically
        static_beginning (Boolean): If Simulation starts with defined values
    """
    # Creating simulation instance
    new_simulation = Simulation("Test Simulation")

    # clearing file with real time chat data
    open('chart_data.txt', 'w').close()

    if random_simulation:
        if constants.SOCIAL_DISTANCE == 0:
            # Generating random positions to use as starting values
            random_tuple_list = generate_random_tuple_list()

        if static_beginning:
            hs_data, imr_data = static_simulation(
                constants.SICK_NBR, constants.IMMMUNE_IMR_NBR, constants.ASYMP_IMR_NBR, constants.MOD_IMR_NBR, constants.HIGH_IMR_NBR, constants.DEAD_IMR_NBR)
            if len(hs_data) != constants.TOTAL_NUMBER_OF_AGENTS or len(imr_data) != constants.TOTAL_NUMBER_OF_AGENTS:
                logging.error(
                    f"The number of HEALTH STATUS ({len(hs_data)}) and IMR ({len(imr_data)}) data must be equal to the Total of AGENTS in the simulation ({constants.TOTAL_NUMBER_OF_AGENTS})")
                sys.exit()

        # Creating agents
        pbar = tqdm(range(constants.TOTAL_NUMBER_OF_AGENTS))
        for _ in pbar:
            if not static_beginning:  # no static values in the begginging
                create_simulation_agents(new_simulation, random_tuple_list)
            else:
                # static values in the begginging
                create_simulation_agents(
                    new_simulation, random_tuple_list, hs_data=hs_data, imr_data=imr_data)
        pbar.set_description("Creating Agents in random positions")

    # getting initial data about simulation
    initial_infected = new_simulation.get_infected_count()
    initial_healthy = new_simulation.get_healthy_count()
    initial_dead = new_simulation.get_dead_count()
    initial_healed = new_simulation.get_healed_count()
    initial_quarentine = new_simulation.get_quarentine_count()

    logging.info(f"Imunne people: {new_simulation.get_immune_people_count()}")
    logging.info(f"Infected people: {initial_infected}")

    # initializing the variables to build final chart
    x = [1]
    y_healthy = [initial_healthy]
    y_infected = [initial_infected]
    y_dead = [initial_dead]
    y_healed = [initial_healed]
    y_quarentine = [initial_quarentine]

    # updating file qith initial values, for live chart
    line = f"{1}, {initial_healthy}, {initial_infected}, {initial_dead}, {initial_healed}, {initial_quarentine}\n"
    with open('chart_data.txt', 'a') as f:
        f.write(line)

    # Running simulation
    for i in range(2, constants.EPISODES + 1):
        # moving agents
        if constants.SOCIAL_DISTANCE_STEP == 0:
            new_simulation.random_step_no_social_distance(
                constants.SIZE, constants.AGENTS_MOVEMENT_PERCENTAGE)
        else:
            new_simulation.random_step(
                constants.RANDOM_LIMIT, constants.SIZE, constants.AGENTS_MOVEMENT_PERCENTAGE)

        # moving people between env and quarentine
        if i > constants.QUARENTINE_DAYS:
            new_simulation.update_quarentine(constants.SIZE)

        # evaluating agents' health and contacts
        new_simulation.update_health_status()

        # healing people
        new_simulation.set_health_status_at_hospital()

        if graphics_simulation:
            show_graphic_simulation(new_simulation)

        infected = new_simulation.get_infected_count()
        healed = new_simulation.get_healed_count()
        healthy = new_simulation.get_healthy_count()
        dead = new_simulation.get_dead_count()
        quarentine = new_simulation.get_quarentine_count()

        # saving data for final chart
        x.append(i)
        y_healthy.append(new_simulation.get_healthy_count())
        y_infected.append(infected)
        y_dead.append(dead)
        y_healed.append(healed)
        y_quarentine.append(quarentine)

        # updating file for live chart
        line = f"{i}, {healthy}, {infected}, {dead}, {healed}, {quarentine}\n"
        with open('chart_data.txt', 'a') as f:
            f.write(line)

        if(infected == 0):
            break

    # adding final chart
    fig2 = plt.figure(num=2, figsize=(
        constants.ALL_DATA_PLOT_FIG_SIZE_X, constants.ALL_DATA_PLOT_FIG_SIZE_Y))
    ax_fig2 = fig2.add_subplot(1, 1, 1)
    ax_fig2.plot(x, y_healthy, 'o-', color='g', label="Healthy")
    ax_fig2.plot(x, y_infected, 'o-', color='r', label="Infected")
    ax_fig2.plot(x, y_dead, 'o-', color='k', label="Dead")
    ax_fig2.plot(x, y_healed, 'o-', color='y', label="Healed")
    ax_fig2.plot(x, y_quarentine, 'o-', color='b',
                 label="People in Quarentine")
    ax_fig2.legend(loc='upper left')
    plt.show()

    # printing data
    # show_detailed_data(y_infected, y_healed, y_healthy, y_dead, new_simulation)


if __name__ == "__main__":
    import argparse
    import sys
    import time

    parser = argparse.ArgumentParser(
        description="Running a simulation for Covid-19 Simulation.")
    parser.add_argument("-r", "--random", action="store_true",
                        help="Runs with Agents initialized at random positions and with random status")
    parser.add_argument("-g", "--graphics", action="store_true",
                        help="Shows Graphics for the simulation")
    parser.add_argument("-s", "--static_beginning", action="store_true",
                        help="Shows Graphics for the simulation")

    args = parser.parse_args()

    print(f"Simulation 1.0")
    main(random_simulation=args.random, graphics_simulation=args.graphics,
         static_beginning=args.static_beginning)
