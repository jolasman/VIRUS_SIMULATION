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

FOUR_PLOTS_FIG_SIZE_X = 12
from constants import SICK, ASYMPTOMATIC, HEALTHY, FOUR_PLOTS_FIG_SIZE_X , FOUR_PLOTS_FIG_SIZE_Y, ALL_DATA_PLOT_FIG_SIZE_X, ALL_DATA_PLOT_FIG_SIZE_Y, SIMULATION_GRAPHICS_SIZE_X, SIMULATION_GRAPHICS_SIZE_Y

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

EPISODES = 30
TOTAL_NUMBER_OF_AGENTS = 500
SIZE = 500
RANDOM_LIMIT = 10
AGENTS_MOVEMENT_PERCENTAGE = 0.8  # percentage of the agents that moves in the step

# BGR
COLORS_DICT = {0: (0, 0, 255),  # red
               1: (0, 115, 255),  # orange
               2: (0, 255, 255),  # yellow
               3: (255, 0, 196),  # purple
               4: (0, 0, 0),  # dead is black
               5: (0, 255, 0)}  # green

HEALTH_ARRAY = [SICK, ASYMPTOMATIC, HEALTHY]
HEALTH_ARRAY_P = [0.01, 0.001, 0.989]  # probabilities of being of one type


def available_random_pos(simulation):
    """
    """
    new_pos_X = 0
    new_pos_Y = 0
    for _ in simulation.agent_list:
        new_pos_X = random.randint(0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
        new_pos_Y = random.randint(0 + RANDOM_LIMIT, SIZE - RANDOM_LIMIT)
        tuple_list = [
            agent_.pos_tuple for agent_ in simulation.agent_list]
        while (new_pos_X, new_pos_Y) in tuple_list or \
            ((new_pos_X + 1, new_pos_Y) in tuple_list) or \
            ((new_pos_X + 2, new_pos_Y) in tuple_list) or \
            ((new_pos_X + 3, new_pos_Y) in tuple_list) or \
            ((new_pos_X + 4, new_pos_Y) in tuple_list) or \
                (new_pos_X <= 0 or new_pos_Y <= 0) or \
                (new_pos_X >= SIZE or new_pos_Y >= SIZE):
            new_pos_X = random.randint(-RANDOM_LIMIT, RANDOM_LIMIT)
            new_pos_Y = random.randint(-RANDOM_LIMIT, RANDOM_LIMIT)

    return new_pos_X, new_pos_Y


def show_graphic_simulation(simulation):
    """
    """
    # starts an rbg of our size
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    for agent in simulation.agent_list:
        env[agent.pos_X][agent.pos_Y] = COLORS_DICT[agent.health_status]

    # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = Image.fromarray(env, 'RGB')
    # resizing so we can see our agent in all its glory.
    img = img.resize((SIMULATION_GRAPHICS_SIZE_X, SIMULATION_GRAPHICS_SIZE_Y))

    cv2.imshow("image", np.array(img))
    cv2.waitKey(200)


def main():
    """
    """
    # Creating simulation instance
    new_simulation = Simulation("Test Simulation")

    # Creating agents
    pbar = tqdm(range(TOTAL_NUMBER_OF_AGENTS))
    for _ in pbar:
        new_pos_X, new_pos_Y = available_random_pos(new_simulation)

        health_value = np.random.choice(
            HEALTH_ARRAY, p=HEALTH_ARRAY_P, size=(1))[0]

        new_simulation.create_agent(
            new_pos_X, new_pos_Y, health_status=health_value)

        pbar.set_description("Creating Agents in random positions")

    logging.info(new_simulation.get_infected())

    # ploting the data, this is a bad way but one that works
    fig = plt.figure(num=1, figsize=(FOUR_PLOTS_FIG_SIZE_X, FOUR_PLOTS_FIG_SIZE_Y))

    ax = fig.add_subplot(4, 1, 1)
    ax2 = fig.add_subplot(4, 1, 2)
    ax3 = fig.add_subplot(4, 1, 3)
    ax4 = fig.add_subplot(4, 1, 4)

    fig.show()
    x = [1]
    y_healthy = [new_simulation.get_healthy()]
    y_infected = [new_simulation.get_infected()]
    y_dead = [new_simulation.get_dead()]
    y_healed = [new_simulation.get_healed()]

    ax.plot(x, y_healthy, color='g', label="Healthy")
    ax2.plot(x, y_infected, color='r', label="Infected")
    ax3.plot(x, y_dead, color='k', label="Dead")
    ax4.plot(x, y_healed, color='y', label="Healed")
    plt.legend(loc='upper left')

    # Running simulation
    for i in range(2, EPISODES + 1):
        # moving agents
        new_simulation.random_step(
            RANDOM_LIMIT, SIZE, AGENTS_MOVEMENT_PERCENTAGE)

        # healing people
        new_simulation.set_health_status_at_hospital()

        show_graphic_simulation(new_simulation)

        x.append(i)
        y_infected.append(new_simulation.get_infected())
        y_healed.append(new_simulation.get_healed())
        y_dead.append(new_simulation.get_dead())
        y_healthy.append(new_simulation.get_healthy())

        # adding more plots
        ax.plot(x, y_healthy, color='g')
        ax2.plot(x, y_infected, color='r')
        ax3.plot(x, y_dead, color='k')
        ax4.plot(x, y_healed, color='y')

        # setting the aces to integers
        gca = fig.gca()
        gca.set_ylim([0, TOTAL_NUMBER_OF_AGENTS + 100])
        gca.yaxis.set_major_locator(MaxNLocator(integer=True))
        gca.xaxis.set_major_locator(MaxNLocator(integer=True))

        fig.canvas.draw()

    fig2 = plt.figure(num=2, figsize=(ALL_DATA_PLOT_FIG_SIZE_X, ALL_DATA_PLOT_FIG_SIZE_Y))
    ax_fig2 = fig2.add_subplot(1, 1, 1)
    ax_fig2.plot(x, y_healthy, 'o-', color='g')
    ax_fig2.plot(x, y_infected, 'o-', color='r')
    ax_fig2.plot(x, y_dead, 'o-', color='k')
    ax_fig2.plot(x, y_healed, 'o-', color='y')
    fig.show()
    plt.show()


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Running a simulation for Covid-19 Simulation.")
    # parser.add_argument("-l", "--loop", action="store_true", help="shows output")

    # args = parser.parse_args()
    # if args.loop:

    print(f"Simulation 1.0")
    main()
