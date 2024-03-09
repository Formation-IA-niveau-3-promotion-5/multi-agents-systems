import mesa
from robots.agents.robots_types import WhiteRobots, YellowRobots, RedRobots
from robots.objects import RadioactiveWaste
from robots.model import RobotsModel


def robots_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is WhiteRobots:
        portrayal["Shape"] = "robots_mission/robots/resources/white_robot.png"
        scale = 0.6
        for i in range(agent.inventory):
            scale += 0.2
        portrayal["scale"] = scale
        portrayal["Layer"] = 1

    if type(agent) is YellowRobots:
        portrayal["Shape"] = "robots_mission/robots/resources/yellow_robot.png"
        scale = 0.6
        for i in range(agent.inventory):
            scale += 0.2
        portrayal["scale"] = scale
        portrayal["Layer"] = 1

    if type(agent) is RedRobots:
        portrayal["Shape"] = "robots_mission/robots/resources/red_robot.png"
        scale = 0.6
        for i in range(agent.inventory):
            scale += 0.2
        portrayal["scale"] = scale
        portrayal["Layer"] = 1

    elif type(agent) is RadioactiveWaste:
        if agent.radioactivity == 0:
            portrayal["Color"] = "Grey"
        elif agent.radioactivity == 1:
            portrayal["Color"] = "Yellow"
        else:
            portrayal["Color"] = "Red"

        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(robots_portrayal, 30, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Waste not processed", "Color": "#AA0000"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "initial_robots": mesa.visualization.Slider("Inital robots population per color", 10, 10, 100),
    "initial_wastes": mesa.visualization.Slider("Initial wastes on grid per color", 20, 10, 300),
}

server = mesa.visualization.ModularServer(
    RobotsModel, [canvas_element, chart_element], "Multi-agents robots clearing nuclear waste", model_params
)
server.port = 8521
