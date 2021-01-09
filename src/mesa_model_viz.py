from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import (
    CanvasGrid,
    ChartModule,
    # BarChartModule,
    PieChartModule
)
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
PIXELS_Y = PIXELS_X // 2

NUMBER_OF_AGENTS = constants.TOTAL_NUMBER_OF_AGENTS

MAX_NUMBER_AGENTS = (SIZE_X ** 2) // 5


RED = "#ff0000"
ORANGE = "#ff9900"
BROWN = "#993300"
BLUE = "#3399ff"
GREEN = "#33cc33"
DARK_BLUE = "#0000ff"


def agent_portrayal(agent) -> dict:
    """Changes the visualization of each agent based on its heath_status.

    Args:
        agent (SimulationAgent): Agent from the simulation.

    Returns:
        dict: portrayal
    """
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.8}

    if agent.get_health_status() == constants.SICK:
        portrayal["Color"] = RED
        portrayal["Layer"] = 5
        portrayal["r"] = 0.6
    elif agent.get_health_status() == constants.ASYMPTOMATIC:
        portrayal["Color"] = ORANGE
        portrayal["Layer"] = 4
        portrayal["r"] = 0.5
    elif agent.get_health_status() == constants.WITH_DISEASES_SEQUELAES:
        portrayal["Color"] = BROWN
        portrayal["Layer"] = 2
        portrayal["r"] = 0.6
    elif agent.get_health_status() == constants.TOTAL_RECOVERY:
        portrayal["Color"] = BLUE
        portrayal["Layer"] = 2
    elif agent.get_health_status() == constants.HEALTHY:
        portrayal["Color"] = GREEN
        portrayal["Layer"] = 4
        portrayal["r"] = 1
    else:
        portrayal["Color"] = "white"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.1

    return portrayal


def run_simulation() -> None:
    """Runs the simulation.
    """
    logger.info(f"Number of Agents: {NUMBER_OF_AGENTS}")

    grid = CanvasGrid(agent_portrayal, SIZE_X, SIZE_Y, PIXELS_X, PIXELS_Y)

    chart_cumulatives = ChartModule([
        {"Label": "Sick Agents",
         "Color": "RED"},
        {"Label": "Recovered Agents",
         "Color": BROWN},
        {"Label": "Dead Agents",
         "Color": "black"},
        {"Label": "Healthy Agents",
         "Color": GREEN},
        {"Label": "Quarantine Agents",
         "Color": DARK_BLUE}
    ],
        # canvas_width=constants.ALL_DATA_PLOT_FIG_SIZE_X,
        # declaring both height and width yields some kind of a bug where the values are random
        canvas_height=constants.ALL_DATA_PLOT_FIG_SIZE_Y,
        data_collector_name='datacollector_currents_prcntg')

    chart_dailys = ChartModule([
        {"Label": "Infected Agents",
         "Color": "RED"},
        {"Label": "Recovered Agents",
         "Color": BROWN},
        {"Label": "Dead Agents",
         "Color": "black"},
        {"Label": "Quarantine Agents",
         "Color": DARK_BLUE}
    ],
        # canvas_width=constants.ALL_DATA_PLOT_FIG_SIZE_X,
        # declaring both height and width yields some kind of a bug where the values are random
        canvas_height=constants.ALL_DATA_PLOT_FIG_SIZE_Y,
        data_collector_name='datacollector_dailys')

    pie_chart_cumulatives = PieChartModule([
        {"Label": "Recovered Agents",
         "Color": DARK_BLUE},
        {"Label": "Dead Agents",
         "Color": "black"},
        {"Label": "Healthy Agents",
         "Color": GREEN}
    ],
        data_collector_name='datacollector_cumulatives_prcntg')

    build_server_sim(grid, chart_cumulatives,
                     chart_dailys, pie_chart_cumulatives)


def build_server_sim(*params) -> None:
    """Builds and runs the server to visualize the simulation and charts.
    """
    global NUMBER_OF_AGENTS
    if NUMBER_OF_AGENTS > MAX_NUMBER_AGENTS:
        NUMBER_OF_AGENTS = MAX_NUMBER_AGENTS

    model_params = {
        "N": UserSettableParameter(
            "slider",
            "Number of agents",
            NUMBER_OF_AGENTS,  # default
            10,  # min
            MAX_NUMBER_AGENTS,  # max
            1,  # step
            description="Choose how many agents to include in the model",
        ),
        "width": SIZE_X,
        "height": SIZE_Y,
        "static": True,
        "sick_p": UserSettableParameter(
            "slider",
            "Percentage of infected (Sick) agents",
            constants.SICK_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of infected (Sick) agents in the model",
        ),
        "aymp_p": UserSettableParameter(
            "slider",
            "Percentage of infected (Asymptomatic) agents",
            constants.ASYMP_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of infected (Asymptomatic) agents in the model",
        ),
        "imr_immune_p": UserSettableParameter(
            "slider",
            "Percentage of immune agents",
            constants.IMMMUNE_IMR_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of immune agents in the model",
        ),
        "imr_asymp_p": UserSettableParameter(
            "slider",
            "Percentage of asymptomatic agents",
            constants.ASYMP_IMR_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of asymptomatic agents in the model",
        ),
        "imr_mod_p": UserSettableParameter(
            "slider",
            "Percentage of moderately infected agents",
            constants.MOD_IMR_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of moderately infected agents in the model",
        ),
        "imr_severe_p": UserSettableParameter(
            "slider",
            "Percentage of severe infected agents",
            constants.SEVERE_IMR_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of severe infected agents in the model",
        ),
        "imr_dead_p": UserSettableParameter(
            "slider",
            "Percentage of dead agents",
            constants.DEAD_IMR_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of dead agents in the model",
        ),
        "wearing_mask": UserSettableParameter(
            "slider",
            "Percentage of agents wearing a mask",
            constants.AGENTS_WEARING_MASK_PRCNTG,
            0,
            1,
            0.1,
            description="Choose how many percentage of agents  wearing a mask in the model",
        )
    }

    server = ModularServer(mesa_model.SimulationModel,
                           params,  # list
                           "COVID-19 Simulation",
                           model_params)  # model parameters

    server.port = 8521  # The default
    server.launch()


if __name__ == "__main__":
    run_simulation()
