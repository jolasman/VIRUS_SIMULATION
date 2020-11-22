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
    SIZE, RANDOM_LIMIT, AGENTS_MOVEMENT_PERCENTAGE, COLORS_DICT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

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
            can_add = False
            for x_ax in range(SOCIAL_DISTANCE + 1):
                for y_ax in range(SOCIAL_DISTANCE + 1):
                    if (new_pos_X + x_ax, new_pos_Y + y_ax) not in tuple_list and \
                            (new_pos_X - x_ax, new_pos_Y - y_ax) not in tuple_list:
                        can_add = True
                    else:
                        can_add = False

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
    logging.info(f" Initial Immune people: {simulation.get_immune_people()}")


def main():
    """
    """
    # Creating simulation instance
    new_simulation = Simulation("Test Simulation")

    # clearing file with real time chat data
    open('chart_data.txt', 'w').close()

    # Creating agents
    pbar = tqdm(range(TOTAL_NUMBER_OF_AGENTS))
    for _ in pbar:
        new_pos_X, new_pos_Y = available_random_pos(new_simulation)

        health_value = np.random.choice(
            HEALTH_ARRAY, p=HEALTH_ARRAY_P, size=(1))[0]

        immune_response_value = np.random.choice(
            IMR_ARRAY, p=IMR_ARRAY_P, size=(1))[0]

        new_simulation.create_agent(
            new_pos_X, new_pos_Y, health_status=health_value, immune_system_response=immune_response_value)

        pbar.set_description("Creating Agents in random positions")


    initial_infected = new_simulation.get_infected()
    initial_healthy = new_simulation.get_healthy()
    initial_dead = new_simulation.get_dead()
    initial_healed = new_simulation.get_healed()
    
    logging.info(f"Imunne people: {new_simulation.get_immune_people()}")
    logging.info(f"Infected people: {initial_infected}")

    x = [1]
    y_healthy = [initial_healthy]
    y_infected = [initial_infected]
    y_dead = [initial_dead]
    y_healed = [initial_healed]

    # updating file for live chart
    line = f"{1}, {initial_healthy}, {initial_infected}, {initial_dead}, {initial_healed}\n"
    with open('chart_data.txt', 'a') as f:
        f.write(line)

    myfile = open('chart_data.txt', 'a')
    # Running simulation
    for i in range(2, EPISODES + 1):
        # moving agents
        new_simulation.random_step(
            RANDOM_LIMIT, SIZE, AGENTS_MOVEMENT_PERCENTAGE)

        # healing people
        new_simulation.set_health_status_at_hospital()

        show_graphic_simulation(new_simulation)

        infected = new_simulation.get_infected()
        healed = new_simulation.get_healed()
        healthy = new_simulation.get_healthy()
        dead = new_simulation.get_dead()

        #saving data for final chart
        x.append(i)
        y_healthy.append(new_simulation.get_healthy())
        y_infected.append(infected)
        y_dead.append(dead)
        y_healed.append(healed)

        # # setting the aces to integers
        # gca = fig.gca()
        # gca.set_ylim([0, TOTAL_NUMBER_OF_AGENTS + 100])
        # gca.yaxis.set_major_locator(MaxNLocator(integer=True))
        # gca.xaxis.set_major_locator(MaxNLocator(integer=True))

        # fig.canvas.draw()

        # updating file for live chart
        line = f"{i}, {healthy}, {infected}, {dead}, {healed}\n"
        with open('chart_data.txt', 'a') as f:
            f.write(line)     

        if(infected == 0):
            break
    

    # adding final chart
    fig2 = plt.figure(num=2, figsize=(
        ALL_DATA_PLOT_FIG_SIZE_X, ALL_DATA_PLOT_FIG_SIZE_Y))
    ax_fig2 = fig2.add_subplot(1, 1, 1)
    ax_fig2.plot(x, y_healthy, 'o-', color='g')
    ax_fig2.plot(x, y_infected, 'o-', color='r')
    ax_fig2.plot(x, y_dead, 'o-', color='k')
    ax_fig2.plot(x, y_healed, 'o-', color='y')
    plt.show()

    # printing data
    #show_detailed_data(y_infected, y_healed, y_healthy, y_dead, new_simulation)


if __name__ == "__main__":
    import argparse
    import sys
    import time

    parser = argparse.ArgumentParser(
        description="Running a simulation for Covid-19 Simulation.")
    # parser.add_argument("-l", "--loop", action="store_true", help="shows output")

    # args = parser.parse_args()
    # if args.loop:

    print(f"Simulation 1.0")
    main()
   
   
    