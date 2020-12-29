from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa_model import MoneyModel


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}
    return portrayal


# let’s create a 10x10 grid, drawn in 500 x 500 pixels.
grid = CanvasGrid(agent_portrayal, 100, 100, 800, 800)

"""
- The model class we’re running and visualizing; in this case, MoneyModel.
- A list of module objects to include in the visualization; here, just [grid]
- The title of the model: “Money Model”
- Any inputs or arguments for the model itself. In this case, 100 agents, and height and width of 10. 
"""
server = ModularServer(MoneyModel,
                       [grid],
                       "Money Model",
                       {"N": 100, "width": 100, "height": 100})
server.port = 8521  # The default
server.launch()
