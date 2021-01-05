from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import mesa_model
import sys
import constants
from threading import Thread

import logging
logging.basicConfig(
    level=constants.LOG_LEVEL,
    filename='logs/mesa_model.log',
    filemode='w',
    format="%(name)s %(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SIZE_X = constants.SIZE
SIZE_Y = SIZE_X
PIXELS_X = constants.PIXELS
PIXELS_Y = PIXELS_X
#NUMBER_OF_AGENTS = (SIZE_X ** 2) // 10
NUMBER_OF_AGENTS = constants.TOTAL_NUMBER_OF_AGENTS


def agent_portrayal(agent) -> dict:
    """Changes the visualization of each agent based on its heath_status.

    Args:
        agent (SimulationAgent): Agent from the simulation.

    Returns:
        dict: portrayal
    """
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.8}

    if agent.get_health_status() == constants.SICK:
        portrayal["Color"] = "#ff0000"  # red
        portrayal["Layer"] = 5
        portrayal["r"] = 0.6
    elif agent.get_health_status() == constants.ASYMPTOMATIC:
        portrayal["Color"] = "#ff9900"  # orange
        portrayal["Layer"] = 4
        portrayal["r"] = 0.5
    elif agent.get_health_status() == constants.WITH_DISEASES_SEQUELAES:
        portrayal["Color"] = "#993300"  # brown
        portrayal["Layer"] = 2
        portrayal["r"] = 0.6
    elif agent.get_health_status() == constants.TOTAL_RECOVERY:
        portrayal["Color"] = "#3399ff"  # blue
        portrayal["Layer"] = 2
    elif agent.get_health_status() == constants.HEALTHY:
        portrayal["Color"] = "#33cc33"  # green
        portrayal["Layer"] = 4
        portrayal["r"] = 1
    else:  # dead
        portrayal["Color"] = "white"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1

    return portrayal


def run_simulation() -> None:
    """Runs the simulation.
    """
    logger.info(f"Number of Agents: {NUMBER_OF_AGENTS}")
    grid = CanvasGrid(agent_portrayal, SIZE_X, SIZE_Y, PIXELS_X, PIXELS_Y)
    chart_cumulatives = ChartModule([{"Label": "Sick Agents",
                                      "Color": "#ff0000"},
                                     {"Label": "Recovered Agents",
                                      "Color": "#993300"},
                                     {"Label": "Dead Agents",
                                      "Color": "black"},
                                     {"Label": "Healthy Agents",
                                      "Color": "#33cc33"},
                                     {"Label": "Quarantine Agents",
                                      "Color": "#0000ff"}
                                     ],
                                    # canvas_width=constants.ALL_DATA_PLOT_FIG_SIZE_X,
                                    # declaring both height and width yields some kind of a bug where the values are random
                                    canvas_height=constants.ALL_DATA_PLOT_FIG_SIZE_Y,
                                    data_collector_name='datacollector_cumulatives')

    build_server_sim(grid, chart_cumulatives)


def build_server_sim(*params) -> None:
    """Builds and runs the server to visualize the simulation and charts.
    """
    server = ModularServer(mesa_model.SimulationModel,
                           params,  # list
                           "Money Model",
                           {"N": NUMBER_OF_AGENTS, "width": SIZE_X, "height": SIZE_Y, "static": False})  # model parameters
    server.port = 8521  # The default
    server.launch()


if __name__ == "__main__":
    run_simulation()
