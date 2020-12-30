from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa_model import SimulationModel
import sys
import constants


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.get_health_status() == constants.SICK:
        portrayal["Color"] = "#ff0000"
        portrayal["Layer"] = 0
        portrayal["r"] = 1
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
    else: #dead
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
grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)

"""
- The model class we’re running and visualizing; in this case, SimulationModel.
- A list of module objects to include in the visualization; here, just [grid]
- The title of the model: “Money Model”
- Any inputs or arguments for the model itself. In this case, 100 agents, and height and width of 10. 
"""
server = ModularServer(SimulationModel,
                       [grid],
                       "Money Model",
                       {"N": 50, "width": 50, "height": 50})
server.port = 8521  # The default
server.launch()
