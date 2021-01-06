import constants
import cv2
import pickle
import random
import time
import sys
import logging
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib import style
from matplotlib.ticker import MaxNLocator
from PIL import Image
style.use('fivethirtyeight')

logging.basicConfig(
    level=constants.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def save_detailed_data(x, daily_infected, daily_dead, daily_healed, daily_quarantine, y_healthy, y_infected, y_dead, y_healed, y_quarantine, static_beginning):
    """Saves cumulative and daily data in charts

    Args:
        x (List): List of days
        daily_infected (List): List of daily infected
        daily_dead (List): List of daily dead
        daily_healed (List): List of daily healed
        daily_quarantine (List): List of daily quarantine
        y_healthy (List): List of cumulative healthy agents
        y_infected (List):  List of cumulative infected agents
        y_dead (List): List of cumulative dead agents
        y_healed (List): List of cumulative healed agents
        y_quarantine (List): List of cumulative quarantine agents
    """
    dict_ = {
        "x": x,
        "daily_infected": daily_infected,
        "daily_dead": daily_dead,
        "daily_healed": daily_healed,
        "daily_quarantine": daily_quarantine,
        "y_healthy": y_healthy,
        "y_infected": y_infected,
        "y_dead": y_dead,
        "y_healed": y_healed,
        "y_quarantine": y_quarantine,
    }
    if static_beginning:
        folder = (f"{constants.PICKLE_DATA}Simulation_{constants.TOTAL_NUMBER_OF_AGENTS}_{constants.SIZE}_{constants.RANDOM_LIMIT}_{constants.AGENTS_MOVEMENT_PERCENTAGE}_{constants.QUARANTINE_PERCENTAGE}_{constants.QUARANTINE_DAYS}"
                  f"_Agent_{constants.HEALTH_ARRAY_P}_{constants.RECOVERY_SEQUELS_P}_{constants.SICK_P}_{constants.ASYMPTOMATIC_P}_{constants.HEALTHY_P}_{constants.SOCIAL_DISTANCE}_{constants.SOCIAL_DISTANCE_STEP}_{constants.CONTAGIOUS_DISTANCE}_"
                  f"{constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED}_{constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD}_{constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS}_{constants.CONTAGIOUS_AGENT_MASK}_{constants.HEALTHY_AGENT_MASK}_"
                  f"{constants.CONTAGIOUS_AGENT_MASK_HEALTHY_MASK}_{constants.CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK}")

        filename = f"{folder}/Static_{constants.SICK_NBR}_{constants.ASYMP_NBR}_{constants.IMMMUNE_IMR_NBR}_{constants.ASYMP_IMR_NBR}_{constants.MOD_IMR_NBR}_{constants.HIGH_IMR_NBR}_{constants.DEAD_IMR_NBR}_{constants.AGENTS_WEARING_MASK}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.pickle"
    else:
        folder = (f"{constants.PICKLE_DATA}Simulation_{constants.TOTAL_NUMBER_OF_AGENTS}_{constants.SIZE}_{constants.RANDOM_LIMIT}_{constants.AGENTS_MOVEMENT_PERCENTAGE}_{constants.QUARANTINE_PERCENTAGE}_{constants.QUARANTINE_DAYS}")

        filename = (f"{folder}/_Agent_{constants.HEALTH_ARRAY_P}_{constants.RECOVERY_SEQUELS_P}_{constants.SICK_P}_{constants.ASYMPTOMATIC_P}_{constants.HEALTHY_P}_{constants.SOCIAL_DISTANCE}_{constants.SOCIAL_DISTANCE_STEP}_{constants.CONTAGIOUS_DISTANCE}_"
                    f"{constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED}_{constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD}_{constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS}_{constants.CONTAGIOUS_AGENT_MASK}_{constants.HEALTHY_AGENT_MASK}_"
                    f"{constants.CONTAGIOUS_AGENT_MASK_HEALTHY_MASK}_{constants.CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.pickle")

    try:
        Path(folder).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logging.error("Can't create {dir}: {err}".format(dir=folder, err=e))
        sys.exit()

    with open(filename, 'wb') as handle:
        pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)


def find_max_list(list_):
    """Returns the length of the biggest list in the list of lists

    Args:
        list_ (List): List of lists

    Returns:
        max (Integer): Biggest list length
    """
    list_len = [len(i) for i in list_]
    return max(list_len)


def calc_mean(list_of_lists, is_X=False):
    """Receives a list of list and returns a list with the mean of each value in the inner lists

    Args:
        list_of_lists (List): List of lists
        is_X (Boolean): If x axis array increments the value

    Returns:
        List: list with the mean of each value in the inner lists of list_of_lists
    """

    if len(list_of_lists) == 0:
        return []

    mean_list = []
    length = find_max_list(list_of_lists)
    for list_ in list_of_lists:
        while len(list_) < length:
            there = True
            if is_X:
                list_.append(list_[-1] + 1)
            else:
                # if there is no value in that simulation we use 0 as daily value
                list_.append(0)
    for i in range(len(list_of_lists[0])):
        mean = 0
        for array in list_of_lists:
            mean += array[i]
        mean /= len(list_of_lists)
        mean_list.append(int(mean))

    return mean_list


def load_detailed_data_average(max_files_nbr, static_beginning):
    """Loads the data and presents the charts

    Args:
        max_files_nbr (Integer): Maximum number of files to use for each type of simulation
        static_beginning (Boolean): If it is a static simulation
    """

    if static_beginning:
        folder = (f"{constants.PICKLE_DATA}Simulation_{constants.TOTAL_NUMBER_OF_AGENTS}_{constants.SIZE}_{constants.RANDOM_LIMIT}_{constants.AGENTS_MOVEMENT_PERCENTAGE}_{constants.QUARANTINE_PERCENTAGE}_{constants.QUARANTINE_DAYS}"
                  f"_Agent_{constants.HEALTH_ARRAY_P}_{constants.RECOVERY_SEQUELS_P}_{constants.SICK_P}_{constants.ASYMPTOMATIC_P}_{constants.HEALTHY_P}_{constants.SOCIAL_DISTANCE}_{constants.SOCIAL_DISTANCE_STEP}_{constants.CONTAGIOUS_DISTANCE}_"
                  f"{constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED}_{constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD}_{constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS}_{constants.CONTAGIOUS_AGENT_MASK}_{constants.HEALTHY_AGENT_MASK}_"
                  f"{constants.CONTAGIOUS_AGENT_MASK_HEALTHY_MASK}_{constants.CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK}")
        filename = f"Static_{constants.SICK_NBR}_{constants.ASYMP_NBR}_{constants.IMMMUNE_IMR_NBR}_{constants.ASYMP_IMR_NBR}_{constants.MOD_IMR_NBR}_{constants.HIGH_IMR_NBR}_{constants.DEAD_IMR_NBR}_{constants.AGENTS_WEARING_MASK}_"
    else:
        folder = (f"{constants.PICKLE_DATA}Simulation_{constants.TOTAL_NUMBER_OF_AGENTS}_{constants.SIZE}_{constants.RANDOM_LIMIT}_{constants.AGENTS_MOVEMENT_PERCENTAGE}_{constants.QUARANTINE_PERCENTAGE}_{constants.QUARANTINE_DAYS}")
        filename = (f"_Agent_{constants.HEALTH_ARRAY_P}_{constants.RECOVERY_SEQUELS_P}_{constants.SICK_P}_{constants.ASYMPTOMATIC_P}_{constants.HEALTHY_P}_{constants.SOCIAL_DISTANCE}_{constants.SOCIAL_DISTANCE_STEP}_{constants.CONTAGIOUS_DISTANCE}_"
                    f"{constants.INFECTED_DAYS_THRESHOLD_FOR_INFECTED}_{constants.INFECTED_DAYS_THRESHOLD_FOR_DEAD}_{constants.INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS}_{constants.CONTAGIOUS_AGENT_MASK}_{constants.HEALTHY_AGENT_MASK}_"
                    f"{constants.CONTAGIOUS_AGENT_MASK_HEALTHY_MASK}_{constants.CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK}_")
    x_arrays = []
    daily_infected_arrays = []
    daily_dead_arrays = []
    daily_healed_arrays = []
    daily_quarantine_arrays = []
    y_healthy_arrays = []
    y_infected_arrays = []
    y_dead_arrays = []
    y_healed_arrays = []
    y_quarantine_arrays = []

    error_msg = f"No old simulation with your current configuration. Please run some new simulations and try again later."
    try:
        os.listdir(folder)
    except:
        logging.error(error_msg)
        sys.exit()

    files_list = []
    # get all files in the folder with the same configurations as the current
    for file_ in os.listdir(folder):
        if filename in file_ and file_[-7:] == ".pickle":
            files_list.append(file_)

    if len(files_list) == 0:
        logging.error(error_msg)
        sys.exit()

    # getting all data from each file
    for count, file_ in enumerate(files_list):
        if count <= max_files_nbr:
            with open(f"{folder}/{file_}", 'rb') as handle:
                dict_ = pickle.load(handle)
                x_arrays.append(dict_["x"])
                daily_infected_arrays.append(dict_["daily_infected"])
                daily_dead_arrays.append(dict_["daily_dead"])
                daily_healed_arrays.append(dict_["daily_healed"])
                daily_quarantine_arrays.append(dict_["daily_quarantine"])
                y_healthy_arrays.append(dict_["y_healthy"])
                y_infected_arrays.append(dict_["y_infected"])
                y_dead_arrays.append(dict_["y_dead"])
                y_healed_arrays.append(dict_["y_healed"])
                y_quarantine_arrays.append(dict_["y_quarantine"])

    x_mean_array = calc_mean(x_arrays, True)
    daily_infected_mean_array = calc_mean(daily_infected_arrays)
    daily_dead_mean_array = calc_mean(daily_dead_arrays)
    daily_healed_mean_array = calc_mean(daily_healed_arrays)
    daily_quarantine_mean_array = calc_mean(daily_quarantine_arrays)
    y_healthy_mean_array = calc_mean(y_healthy_arrays)
    y_infected_mean_array = calc_mean(y_infected_arrays)
    y_dead_mean_array = calc_mean(y_dead_arrays)
    y_healed_mean_array = calc_mean(y_healed_arrays)
    y_quarantine_mean_array = calc_mean(y_quarantine_arrays)

    logging.info(
        f"Average number of total new infected agents: {sum(daily_infected_mean_array) - daily_infected_mean_array[0]}")
    logging.info(
        f"Average number of total new dead agents: {sum(daily_dead_mean_array) - daily_dead_mean_array[0]}")

    return x_mean_array, daily_infected_mean_array, daily_dead_mean_array, daily_healed_mean_array, daily_quarantine_mean_array, y_healthy_mean_array, y_infected_mean_array, y_dead_mean_array, y_healed_mean_array, y_quarantine_mean_array


def load_detailed_data_file(filename):
    """Loads the data and presents the charts for a specific file

    Args:
        max_filesfilename_nbr (String): File to load data
    """
    if not os.path.exists(f"../{filename}"):
        logging.error(f"Cannot find the file.")
        sys.exit()

    # getting all data from  file
    with open(f"../{filename}", 'rb') as handle:
        dict_ = pickle.load(handle)
        x_array = dict_["x"]
        daily_infected_array = dict_["daily_infected"]
        daily_dead_array = dict_["daily_dead"]
        daily_healed_array = dict_["daily_healed"]
        daily_quarantine_array = dict_["daily_quarantine"]
        y_healthy_array = dict_["y_healthy"]
        y_infected_array = dict_["y_infected"]
        y_dead_array = dict_["y_dead"]
        y_healed_array = dict_["y_healed"]
        y_quarantine_array = dict_["y_quarantine"]

    return x_array, daily_infected_array, daily_dead_array, daily_healed_array, daily_quarantine_array, y_healthy_array, y_infected_array, y_dead_array, y_healed_array, y_quarantine_array


def show_detailed_data(x, daily_infected, daily_dead, daily_healed, daily_quarantine, y_healthy, y_infected, y_dead, y_healed, y_quarantine, can_plot, filename=False):
    """Shows cumulative and daily data in charts

    Args:
        x (List): List of days
        daily_infected (List): List of daily infected
        daily_dead (List): List of daily dead
        daily_healed (List): List of daily healed
        daily_quarantine (List): List of daily quarantine
        y_healthy (List): List of cumulative healthy agents
        y_infected (List):  List of cumulative infected agents
        y_dead (List): List of cumulative dead agents
        y_healed (List): List of cumulative healed agents
        y_quarantine (List): List of cumulative quarantine agents
    """
    if can_plot:
        # adding final chart
        fig2Title = f"{filename} 1" if filename else 1
        fig2 = plt.figure(num=fig2Title, figsize=(
            constants.ALL_DATA_PLOT_FIG_SIZE_X, constants.ALL_DATA_PLOT_FIG_SIZE_Y))
        ax_fig2 = fig2.add_subplot(1, 1, 1)
        ax_fig2.plot(x, y_healthy, 'o-', color='g', label="Healthy")
        ax_fig2.plot(x, y_infected, 'o-', color='r', label="Infected")
        ax_fig2.plot(x, y_dead, 'o-', color='k', label="Dead")
        ax_fig2.plot(x, y_healed, 'o-', color='y', label="Healed")
        ax_fig2.plot(x, y_quarantine, 'o-', color='b',
                     label="People in Quarentine")
        ax_fig2.legend(loc='upper left')
        ax_fig2.set_xlabel('Days')
        ax_fig2.set_ylabel('Agents')
        fig2.suptitle('Simulation cumulative values', fontsize=16)

        fig3Title = f"{filename} 2" if filename else 2
        fig3 = plt.figure(num=fig3Title, figsize=(
            constants.ALL_DATA_PLOT_FIG_SIZE_X, constants.ALL_DATA_PLOT_FIG_SIZE_Y))
        ax_fig3 = fig3.add_subplot(4, 1, 1)
        ax1_fig3 = fig3.add_subplot(4, 1, 2)
        ax2_fig3 = fig3.add_subplot(4, 1, 3)
        ax3_fig3 = fig3.add_subplot(4, 1, 4)
        ax_fig3.plot(x, daily_infected, 'o-', color='r', label="Infected")
        ax1_fig3.plot(x, daily_dead, 'o-', color='k', label="Dead")
        ax2_fig3.plot(x, daily_healed, 'o-', color='y', label="Healed")
        ax3_fig3.plot(x, daily_quarantine, 'o-', color='b',
                      label="Quarentine")
        ax_fig3.legend(loc='upper left')
        ax1_fig3.legend(loc='upper left')
        ax2_fig3.legend(loc='upper left')
        ax3_fig3.legend(loc='upper left')

        ax_fig3.set_xlabel('Days')
        ax1_fig3.set_xlabel('Days')
        ax2_fig3.set_xlabel('Days')
        ax3_fig3.set_xlabel('Days')

        ax_fig3.set_ylabel('Agents')
        ax1_fig3.set_ylabel('Agents')
        ax2_fig3.set_ylabel('Agents')
        ax3_fig3.set_ylabel('Agents')

        fig3.suptitle('Daily Values', fontsize=16)
        plt.show()


def show_graphic_simulation(simulation):
    """Builds an image to represent the environment graphically and displays it

    Args:
        simulation (Simulation): Instance of Simulation class
    """
    # starts an rbg of our size
    env = np.zeros((constants.SIZE, constants.SIZE, 3), dtype=np.uint8)
    for agent in simulation.agent_list:
        # agents with negative coords are dead or in quarantine
        if agent.pos_tuple > (0, 0):
            env[agent.pos_X][agent.pos_Y] = constants.COLORS_DICT[agent.health_status]

    # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = Image.fromarray(env, 'RGB')
    # resizing so we can see our agent in all its glory.
    img = img.resize((constants.SIMULATION_GRAPHICS_SIZE_X,
                      constants.SIMULATION_GRAPHICS_SIZE_Y))

    cv2.imshow("image", np.array(img))
    cv2.waitKey(200)


def static_simulation(sick_prcntg, asymp_prcntg, immmune_imr_prcntg, asymp_imr_prcntg, mod_imr_prcntg, high_imr_prcntg, dead_imr_prcntg, wear_mask_prcntg):
    """ Defining number of people for sick healthy and immune people

    Args:
        * sick_prcntg (Float): percentage of sick agents from total number of agents
        * immmune_imr_prcntg (Float): percentage of agents with immune resposnse system as IMR_IMMUNE from the total number of agents
        * asymp_imr_prcntg (Float): percentage of agents with immune resposnse system as IMR_ASYMPTOMATIC from the total number of agents
        * mod_imr_prcntg (Float): percentage of agents with immune resposnse system as IMR_MODERATELY_INFECTED from the total number of agents
        * high_imr_prcntg (Float): percentage of agents with immune resposnse system as IMR_HIGHLY_INFECTED from the total number of agents
        * dead_imr_prcntg (Float): percentage of agents with immune resposnse system as IMR_DEADLY_INFECTED from the total number of agents

    Returns:
       hs_array (List), imr_array (List), mask_array(List): The three arrays with the data to use
    """
    # heath status
    agents_total = constants.TOTAL_NUMBER_OF_AGENTS
    sick_nbr = math.floor(agents_total * sick_prcntg)
    asymp_nbr = math.floor(agents_total * asymp_prcntg)

    sick_array = [constants.SICK for x in range(sick_nbr)]
    asymp_array = [constants.ASYMPTOMATIC for x in range(asymp_nbr)]
    healthy_array = [constants.HEALTHY for x in range(
        constants.TOTAL_NUMBER_OF_AGENTS - (sick_nbr + asymp_nbr))]

    # IMR
    immmune_imr_nbr = math.floor(agents_total * immmune_imr_prcntg)
    asymp_imr_nbr = math.floor(agents_total * asymp_imr_prcntg)
    mod_imr_nbr = math.floor(agents_total * mod_imr_prcntg)
    high_imr_nbr = math.floor(agents_total * high_imr_prcntg)
    dead_imr_nbr = math.floor(agents_total * dead_imr_prcntg)
    
    imr_totals = immmune_imr_nbr + asymp_imr_nbr + \
        mod_imr_nbr + high_imr_nbr + dead_imr_nbr
    
    if agents_total != imr_totals:
        diff = agents_total - \
            (immmune_imr_nbr + asymp_imr_nbr +
             mod_imr_nbr + high_imr_nbr + dead_imr_nbr)
        # fixing approximation issues by adding the diff to the dead imr number
        dead_imr_nbr += diff
        
    # using healthy agents after imunne number
    # second part of list, starting after the last immmune_imr_nbr
    virus_array = healthy_array[:immmune_imr_nbr] + sick_array + asymp_array
    random.shuffle(virus_array)
    # this aligns the hs_array and the imr_array to get healthy people being immune. otherwise, we could get an infected agent with IMR of immune
    hs_array = healthy_array[immmune_imr_nbr:] + virus_array
    # I do not suffle the hs_array and imr_array to guarantee that only the healty agents are immune

    immune_array = [constants.IMR_IMMUNE for x in range(immmune_imr_nbr)]
    asymp_array = [constants.IMR_ASYMPTOMATIC for x in range(asymp_imr_nbr)]
    mod_array = [constants.IMR_MODERATELY_INFECTED for x in range(mod_imr_nbr)]
    high_array = [constants.IMR_HIGHLY_INFECTED for x in range(high_imr_nbr)]
    dead_array = [constants.IMR_DEADLY_INFECTED for x in range(dead_imr_nbr)]
    
    non_imunne_array = asymp_array + mod_array + high_array + dead_array
    random.shuffle(non_imunne_array)
    # this aligns the hs_array and the imr_array to get healthy people being immune. otherwise, we could get an infected agent with IMR of immune
    imr_array = immune_array + non_imunne_array
    # I do not suffle the hs_array and imr_array to guarantee that only the healty agents are immune
    
    # wearing mask
    wear_mask_nbr = math.floor(agents_total * wear_mask_prcntg)
    
    wear_mask_array = [True for x in range(wear_mask_nbr)]
    no_mask_array = [False for x in range(
        constants.TOTAL_NUMBER_OF_AGENTS - wear_mask_nbr)]
    
    mask_array = wear_mask_array + no_mask_array
    random.shuffle(mask_array)

    return hs_array, imr_array, mask_array


def generate_random_tuple_list():
    """Builds a list with unique values of X and Y coordinates as tuples

    Returns:
        tuple_list (Tuple): Tuple of runique random positions
    """
    tuple_list = set()
    while len(tuple_list) < constants.TOTAL_NUMBER_OF_AGENTS:
        x = random.randint(0 + constants.RANDOM_LIMIT,
                           constants.SIZE-constants.RANDOM_LIMIT)
        y = random.randint(0 + constants.RANDOM_LIMIT,
                           constants.SIZE-constants.RANDOM_LIMIT)
        tuple_list.add((x, y))

    tuple_list = list(tuple_list)
    random.shuffle(tuple_list)

    return tuple_list


def get_random_pos(random_tuple_list):
    """Returns the last tuple as x and y variables for the given list of tuples

    Args:
        random_tuple_list (List): List of tuples (x,y)

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
        new_pos_X = random.randint(
            0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
        new_pos_Y = random.randint(
            0 + constants.RANDOM_LIMIT, constants.SIZE - constants.RANDOM_LIMIT)
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


def create_simulation_agents(new_simulation, random_tuple_list, hs_data=None, imr_data=None, mask_data=None):
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

    if mask_data is None:
        wear_mask = None
    else:
        wear_mask = mask_data.pop()

    new_simulation.create_agent(
        new_pos_X, new_pos_Y, health_status=health_value, immune_system_response=immune_response_value, wear_mask=wear_mask)
