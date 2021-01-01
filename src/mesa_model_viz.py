from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa_model import SimulationModel
import sys
import constants

SIZE_X = 30
SIZE_Y = 30
PIXELS_X = 500
PIXELS_Y = 500
NUMBER_OF_AGENTS = 50


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.8}

    if agent.get_health_status() == constants.SICK:
        portrayal["Color"] = "#ff0000"
        portrayal["Layer"] = 5
        portrayal["r"] = 0.4
    elif agent.get_health_status() == constants.ASYMPTOMATIC:
        portrayal["Color"] = "#ff9900"
        portrayal["Layer"] = 1
    elif agent.get_health_status() == constants.WITH_DISEASES_SEQUELAES:
        portrayal["Color"] = "#ff6699"
        portrayal["Layer"] = 2
    elif agent.get_health_status() == constants.TOTAL_RECOVERY:
        portrayal["Color"] = "#3399ff"
        portrayal["Layer"] = 3
    elif agent.get_health_status() == constants.HEALTHY:
        portrayal["Color"] = "#33cc33"
        portrayal["Layer"] = 4
        portrayal["r"] = 1
    else:  # dead
        portrayal["Color"] = "white"
        portrayal["Layer"] = 4
        portrayal["r"] = 0.1

    # portrayal = {"Shape": "circle",
    #              "Color": "red",
    #              "Filled": "true",
    #              "Layer": 0,
    #              "r": 0.5}

    print(portrayal)

    return portrayal


# let’s create a 10x10 grid, drawn in 500 x 500 pixels.
grid = CanvasGrid(agent_portrayal, SIZE_X, SIZE_Y, PIXELS_X, PIXELS_Y)

chart_sick = ChartModule([{"Label": "Sick Agents",
                           "Color": "#ff0000"}],
                         data_collector_name='datacollector_sick')
chart_recover = ChartModule([{"Label": "Recovered Agents",
                              "Color": "#ff6699"}],
                            data_collector_name='datacollector_recover')
chart_dead = ChartModule([{"Label": "Dead Agents",
                           "Color": "black"}],
                         data_collector_name='datacollector_dead')
chart_healthy = ChartModule([{"Label": "Healthy Agents",
                              "Color": "#33cc33"}],
                            data_collector_name='datacollector_healthy')

"""
- The model class we’re running and visualizing; in this case, SimulationModel.
- A list of module objects to include in the visualization; here, just [grid]
- The title of the model: “Money Model”
- Any inputs or arguments for the model itself. In this case, 100 agents, and height and width of 10. 
"""
server = ModularServer(SimulationModel,
                       [grid, chart_sick, chart_recover,
                           chart_dead, chart_healthy],
                       "Money Model",
                       {"N": NUMBER_OF_AGENTS, "width": SIZE_X, "height": SIZE_Y})
server.port = 8521  # The default
server.launch()
