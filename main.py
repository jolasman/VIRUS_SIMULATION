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
from matplotlib.ticker import MaxNLocator

from constants import SICK, ASYMPTOMATIC, HEALTHY, FOUR_PLOTS_FIG_SIZE_X, FOUR_PLOTS_FIG_SIZE_Y, ALL_DATA_PLOT_FIG_SIZE_X, ALL_DATA_PLOT_FIG_SIZE_Y, \
    SIMULATION_GRAPHICS_SIZE_X, SIMULATION_GRAPHICS_SIZE_Y, IMR_ARRAY, IMR_ARRAY_P, HEALTH_ARRAY, HEALTH_ARRAY_P, SOCIAL_DISTANCE, EPISODES, TOTAL_NUMBER_OF_AGENTS, \
    SIZE, RANDOM_LIMIT, AGENTS_MOVEMENT_PERCENTAGE, COLORS_DICT, SOCIAL_DISTANCE_STEP, QUARENTINE_DAYS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)

# TODO
# Quarentine for people
# Age based Immune system


def generate_random_tuple_list():
    """
    """
    tuple_list = set()
    while len(tuple_list) < TOTAL_NUMBER_OF_AGENTS:
        x = random.randint(0 + RANDOM_LIMIT, SIZE-RANDOM_LIMIT)
        y = random.randint(0 + RANDOM_LIMIT, SIZE-RANDOM_LIMIT)
        tuple_list.add((x, y))

    tuple_list = list(tuple_list)
    random.shuffle(tuple_list)

    return tuple_list


def get_random_pos(random_tuple_list):
    """
    """
    (new_pos_X, new_pos_Y) = random_tuple_list.pop()
    return new_pos_X, new_pos_Y


def available_random_pos(simulation):
    """
    """
    new_pos_X = 0
    new_pos_Y = 0
    has_value = False
    for _ in simulation.agent_list:
        new_pos_X = random.randint(0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
        new_pos_Y = random.randint(0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
        tuple_list = [
            agent_.pos_tuple for agent_ in simulation.agent_list]
        while not has_value:
            can_add = True
            x_loop_must_break = False
            for x_ax in range(SOCIAL_DISTANCE + 1):
                for y_ax in range(SOCIAL_DISTANCE + 1):
                    if (new_pos_X + x_ax, new_pos_Y + y_ax) in tuple_list or \
                        (new_pos_X + x_ax, new_pos_Y - y_ax) in tuple_list or \
                        (new_pos_X - x_ax, new_pos_Y + y_ax) in tuple_list or\
                            (new_pos_X - x_ax, new_pos_Y - y_ax) in tuple_list:
                        can_add = False
                        x_loop_must_break = True
                if x_loop_must_break:
                    break

            if can_add and (new_pos_X >= SIZE or new_pos_Y >= SIZE):
                can_add = False

            if not can_add:
                new_pos_X = random.randint(
                    0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
                new_pos_Y = random.randint(
                    0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
            else:
                has_value = True

    return new_pos_X, new_pos_Y


def show_graphic_simulation(simulation):
    """
    """
    # starts an rbg of our size
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    for agent in simulation.agent_list:
        # agents with negative coords are dead or in quarentine
        if agent.pos_tuple > (0, 0):
            env[agent.pos_X][agent.pos_Y] = COLORS_DICT[agent.health_status]

    # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = Image.fromarray(env, 'RGB')
    # resizing so we can see our agent in all its glory.
    img = img.resize((SIMULATION_GRAPHICS_SIZE_X, SIMULATION_GRAPHICS_SIZE_Y))

    cv2.imshow("image", np.array(img))
    cv2.waitKey(200)


def show_detailed_data(infected, healed, healthy, dead, simulation):
    """
    """
    logging.info(f" Total Infected people: {sum(infected)}")
    logging.info(f" Total Healed people: {sum(healed)}")
    logging.info(f" Remaining Healthy people: {sum(healthy)}")
    logging.info(f" Total Dead people: {sum(dead)}")
    logging.info(
        f" Initial Immune people: {simulation.get_immune_people_count()}")


def create_simulation_agents(new_simulation, random_tuple_list):
    """
    """
    if SOCIAL_DISTANCE == 0:
        new_pos_X, new_pos_Y = get_random_pos(random_tuple_list)
    else:
        new_pos_X, new_pos_Y = available_random_pos(new_simulation)

    health_value = np.random.choice(
        HEALTH_ARRAY, p=HEALTH_ARRAY_P, size=(1))[0]

    # immune_response_value = np.random.choice(
    #     IMR_ARRAY, p=IMR_ARRAY_P, size=(1))[0]

    # new_simulation.create_agent(
    #     new_pos_X, new_pos_Y, health_status=health_value, immune_system_response=immune_response_value)

    new_simulation.create_agent(
        new_pos_X, new_pos_Y, health_status=health_value)


def main(random_simulation, graphics_simulation):
    """
    """
    # Creating simulation instance
    new_simulation = Simulation("Test Simulation")

    # clearing file with real time chat data
    open('chart_data.txt', 'w').close()

    if random_simulation:
        if SOCIAL_DISTANCE == 0:
            # Generating random positions to use as starting values
            random_tuple_list = generate_random_tuple_list()

        # Creating agents
        pbar = tqdm(range(TOTAL_NUMBER_OF_AGENTS))
        for _ in pbar:
            create_simulation_agents(new_simulation, random_tuple_list)
            pbar.set_description("Creating Agents in random positions")
    else:
        logging.error(f"Not implement yet")
        sys.exit()

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
    for i in range(2, EPISODES + 1):
        # moving agents
        if SOCIAL_DISTANCE_STEP == 0:
            new_simulation.random_step_no_social_distance(
                RANDOM_LIMIT, SIZE, AGENTS_MOVEMENT_PERCENTAGE)
        else:
            new_simulation.random_step(
                RANDOM_LIMIT, SIZE, AGENTS_MOVEMENT_PERCENTAGE)

        # moving people between env and quarentine
        if i > QUARENTINE_DAYS:
            new_simulation.update_quarentine(SIZE)

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
        ALL_DATA_PLOT_FIG_SIZE_X, ALL_DATA_PLOT_FIG_SIZE_Y))
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
    #show_detailed_data(y_infected, y_healed, y_healthy, y_dead, new_simulation)


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

    args = parser.parse_args()

    print(f"Simulation 1.0")
    main(random_simulation=args.random, graphics_simulation=args.graphics)
