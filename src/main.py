__author__ = "Joel Carneiro"
__copyright__ = "Copyright 2020, Open Source Project"
__credits__ = ["Joel Carneiro"]
__license__ = "Apache License 2.0"
__version__ = "1.0"
__maintainer__ = "Joel Carneiro"
__email__ = "jolasman@hotmail.com"
__status__ = "Development"

import constants
import argparse
import sys
import logging
import time
import datetime
import utils
from tqdm import tqdm
from simulation import Simulation

logging.basicConfig(
    level=constants.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def run_simulation(random_simulation, graphics_simulation, static_beginning, daily_data, multi_simulation_nbr):
    """Runs the simulation

    Args:
        random_simulation (Boolean): If simulation agent's movement is random based
        graphics_simulation (Boolean): If show the environment graphically
        static_beginning (Boolean): If Simulation starts with defined values
        daily_data (Boolean): Stores chart data and shows plots at the end
        multi_simulation_nbr (Integer, optional): Number os simulations to run in one script exacution. Defaults to 0.
    """

    # Creating simulation instance
    new_simulation = Simulation("Test Simulation")

    # clearing file with real time chat data
    open(constants.CHART_DATA, 'w').close()

    if random_simulation:
        # Generating random positions to use as starting values
        random_tuple_list = utils.generate_random_tuple_list(
        ) if constants.SOCIAL_DISTANCE == 0 else None

        if static_beginning:
            healty_agents = constants.TOTAL_NUMBER_OF_AGENTS - \
                (constants.SICK_NBR + constants.ASYMP_NBR)
            if healty_agents < constants.IMMMUNE_IMR_NBR:  # immune people are healthy
                logging.error(
                    f"The number of HEALTHY agents ({healty_agents}) cannot be less than the number of immune agents ({constants.IMMMUNE_IMR_NBR})")
                sys.exit()

            hs_data, imr_data, mask_data = utils.static_simulation(
                constants.SICK_NBR, constants.ASYMP_NBR, constants.IMMMUNE_IMR_NBR, constants.ASYMP_IMR_NBR, constants.MOD_IMR_NBR, constants.HIGH_IMR_NBR, constants.DEAD_IMR_NBR, constants.AGENTS_WEARING_MASK)
            if len(hs_data) != constants.TOTAL_NUMBER_OF_AGENTS or len(imr_data) != constants.TOTAL_NUMBER_OF_AGENTS:
                logging.error(
                    f"The number of HEALTH STATUS ({len(hs_data)}) and IMR ({len(imr_data)}) data must be equal to the Total of AGENTS in the simulation ({constants.TOTAL_NUMBER_OF_AGENTS})")
                sys.exit()
        # Creating agents
        pbar = tqdm(range(constants.TOTAL_NUMBER_OF_AGENTS))
        for _ in pbar:
            if not static_beginning:  # no static values in the begginging
                utils.create_simulation_agents(
                    new_simulation, random_tuple_list)
            else:
                # static values in the begginging
                utils.create_simulation_agents(
                    new_simulation, random_tuple_list, hs_data=hs_data, imr_data=imr_data, mask_data=mask_data)
        pbar.set_description("Creating Agents in random positions")
    else:
        logging.error(
            f"Not implemented yet. The Agents can only move in a random way")
        sys.exit()

    # getting initial data about simulation
    initial_infected = new_simulation.get_infected_count()
    initial_healthy = new_simulation.get_healthy_count()
    initial_dead = new_simulation.get_dead_count()
    initial_healed = new_simulation.get_healed_count()
    initial_quarantine = new_simulation.get_quarantine_count()

    logging.info(f"Imunne people: {new_simulation.get_immune_people_count()}")
    logging.info(f"Infected people: {initial_infected}")
    logging.info(
        f"People wearing a mask: {new_simulation.get_wearing_mask_count()}")

    # initializing the variables to build final chart
    x = [1]
    y_healthy = [initial_healthy]
    y_infected = [initial_infected]
    y_dead = [initial_dead]
    y_healed = [initial_healed]
    y_quarantine = [initial_quarantine]

    # updating file qith initial values, for live chart
    line = f"{1}, {initial_healthy}, {initial_infected}, {initial_dead}, {initial_healed}, {initial_quarantine}\n"
    with open(constants.CHART_DATA, 'a') as f:
        f.write(line)

    if daily_data:
        daily_infected = [initial_infected]
        daily_healed = [initial_healed]
        daily_dead = [initial_dead]
        daily_quarantine = [initial_quarantine]

    # Running simulation
    for i in range(2, constants.EPISODES + 1):
        # moving agents
        if constants.SOCIAL_DISTANCE_STEP == 0:
            new_simulation.random_step_no_social_distance(
                constants.SIZE, constants.AGENTS_MOVEMENT_PERCENTAGE)
        else:
            new_simulation.random_step(
                constants.RANDOM_LIMIT, constants.SIZE, constants.AGENTS_MOVEMENT_PERCENTAGE)

        # moving people between env and quarantine
        if i > constants.QUARANTINE_DAYS:
            new_simulation.update_quarantine(constants.SIZE)

        # evaluating agents' health and contacts
        new_simulation.update_health_status()

        # healing people
        new_simulation.set_health_status_by_day()

        if graphics_simulation:
            utils.show_graphic_simulation(new_simulation)

        infected = new_simulation.get_infected_count()
        healed = new_simulation.get_healed_count()
        healthy = new_simulation.get_healthy_count()
        dead = new_simulation.get_dead_count()
        quarantine = new_simulation.get_quarantine_count()

        # saving data for final chart
        x.append(i)
        y_healthy.append(new_simulation.get_healthy_count())
        y_infected.append(infected)
        y_dead.append(dead)
        y_healed.append(healed)
        y_quarantine.append(quarantine)

        if daily_data:
            # saving daily
            new_daily_infected, new_daily_healed, new_daily_dead, new_daily_quarantine = new_simulation.get_daily_data()

            daily_healed.append(new_daily_healed)
            daily_dead.append(new_daily_dead)
            daily_quarantine.append(new_daily_quarantine)
            daily_infected.append(new_daily_infected)
            # resetting values to 0 in each day
            new_simulation.reset_daily_data()

        # updating file for live chart
        line = f"{i}, {healthy}, {infected}, {dead}, {healed}, {quarantine}\n"
        with open(constants.CHART_DATA, 'a') as f:
            f.write(line)

        if(infected == 0):
            logging.info(f"Number of infected agents is now zero")
            break

    if daily_data:
        if multi_simulation_nbr and multi_simulation_nbr > 1:
            can_plot = False
        else:
            can_plot = True

        utils.show_detailed_data(x, daily_infected, daily_dead, daily_healed,
                                 daily_quarantine, y_healthy, y_infected, y_dead, y_healed, y_quarantine, can_plot)
        utils.save_detailed_data(x, daily_infected, daily_dead, daily_healed,
                                 daily_quarantine, y_healthy, y_infected, y_dead, y_healed, y_quarantine, static_beginning)


def main(random_simulation, graphics_simulation, static_beginning, daily_data, load_average_simulations, max_files_nbr, multi_simulation_nbr, load_file):
    """Runs the simulation n times

    Args:
        random_simulation (Boolean): If simulation agent's movement is random based
        graphics_simulation (Boolean): If show the environment graphically
        static_beginning (Boolean): If Simulation starts with defined values
        daily_data (Boolean): Stores chart data and shows plots at the end
        average_simulations (Boolean): Uses saved simulations by averaging its values
        max_files_nbr (Integer): Number of files to use in mean calculus when average_simulations is True
        multi_simulation_nbr (Integer, optional): Number os simulations to run in one script exacution.
    """
    if load_average_simulations:
        if multi_simulation_nbr and multi_simulation_nbr > 1:
            can_plot = False
        else:
            can_plot = True
        utils.show_detailed_data(
            *utils.load_detailed_data_average(max_files_nbr, static_beginning), can_plot)
    elif load_file:
        utils.show_detailed_data(
            *utils.load_detailed_data_file(load_file), True, load_file)
    else:
        if not multi_simulation_nbr:
            multi_simulation_nbr = 1

        time_array = []
        for i in range(multi_simulation_nbr):
            logging.info(
                f"Running Simulation number {i + 1}/{multi_simulation_nbr}")
            start = time.time()
            run_simulation(random_simulation, graphics_simulation, static_beginning,
                           daily_data, multi_simulation_nbr)
            end = time.time()
            execution = end - start
            time_array.append(execution)
            logging.info(
                f"Simulation took: {datetime.timedelta(seconds=execution)}")

        logging.info(
            f"Simulations total time: {datetime.timedelta(seconds=sum(time_array))}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Running a simulation for Covid-19 Simulation.")
    # parser.add_argument("-r", "--random", action="store_true",
    #                     help="runs with agents initialized at random positions and moving randomly")
    parser.add_argument("-g", "--graphics", action="store_true",
                        help="shows graphics for the simulation")
    parser.add_argument("-s", "--static_beginning", action="store_true",
                        help="using the config.yaml file's static section as the starting values for the simulation")
    parser.add_argument("-d", "--daily_data", action="store_true",
                        help="shows the daily numbers for each status (infected, quarantine, healed, etc) and stores the data in files")
    parser.add_argument("-l", "--load_average_simulations", action="store_true",
                        help="uses old simulations of same type and shows the average of all values")
    parser.add_argument("-max", "--max_files_nbr", type=int,
                        help="maximum number of simulations to use. If --load_average_simulations is present this value is required")
    parser.add_argument("-multi", "--multi_simulation_nbr", type=int,
                        help="number of simulations to run in one execution.")
    parser.add_argument("-lf", "--load_file", type=str,
                        help="File path to visualize data.")

    args = parser.parse_args()

    if args.load_average_simulations and not args.max_files_nbr:
        parser.error("--load_average_simulations requires --max_files_nbr")
    if args.multi_simulation_nbr and args.load_average_simulations:
        parser.error(
            "--multi_simulation_nbr and --load_average_simulations cannot be used at same time")
    if args.multi_simulation_nbr and args.multi_simulation_nbr > 1 and not args.daily_data:
        parser.error(
            "--multi_simulation_nbr and --daily_data must be used at same time")

    if args.load_file:
        if args.daily_data or args.load_average_simulations or args.max_files_nbr or args.graphics or args.multi_simulation_nbr:
            parser.error(
                "--load_file is a stand alone argument.")

    logging.info(f"{constants.APP_NAME} {__version__}")
   
    from mesa_handler import MoneyModel
    empty_model = MoneyModel(10)
    empty_model.step()
    