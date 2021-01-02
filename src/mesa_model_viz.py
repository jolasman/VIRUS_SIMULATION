from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import mesa_model
import sys
import constants

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
NUMBER_OF_AGENTS = (SIZE_X ** 2) // 10
# NUMBER_OF_AGENTS = constants.TOTAL_NUMBER_OF_AGENTS

logger.info(f"Number of Agents: {NUMBER_OF_AGENTS}")


def agent_portrayal(agent) -> dict:
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


# let’s create a 10x10 grid, drawn in 500 x 500 pixels.
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
                         data_collector_name='datacollector_cumulatives')


"""
- The model class we’re running and visualizing; in this case, SimulationModel.
- A list of module objects to include in the visualization; here, just [grid]
- The title of the model: “Money Model”
- Any inputs or arguments for the model itself. In this case, 100 agents, and height and width of 10. 
"""
server = ModularServer(mesa_model.SimulationModel,
                       [grid, chart_cumulatives],
                       "Money Model",
                       {"N": NUMBER_OF_AGENTS, "width": SIZE_X, "height": SIZE_Y})
server.port = 8521  # The default
server.launch()
