import mesa

from robots.agents.robots_types import WhiteRobots, YellowRobots, RedRobots
from robots.agents.robot import Robot
from robots.message.Message import Message
from robots.message.MessageService import MessageService
from .objects import RadioactiveWaste
from .scheduler import RandomActivationByTypeFiltered

class RobotsModel(mesa.Model):
    step_count = 0

    description = (
        "A model for simulating robots clearing nuclear waste."
    )

    def exchange_message(self, speakingRobot, messageType):
        neighborhood = self.grid.get_neighborhood(speakingRobot.pos, speakingRobot.moore, True)
        for cell in neighborhood:
            cell_content = self.grid.get_cell_list_contents(cell)
            robots = [obj for obj in cell_content if isinstance(obj, Robot)]
            for robot in robots:
                speakingRobot.send_message(Message(speakingRobot.get_name(), robot.get_name(), messageType, speakingRobot.get_name()))


    def wastesInPos(self, pos):
        this_cell = self.grid.get_cell_list_contents([pos])
        wastes = [obj for obj in this_cell if isinstance(obj, RadioactiveWaste)]
        return wastes
    
    def addWaste(self, pos, radioactivity):
        radioactiveWaste = RadioactiveWaste(self.next_id(), pos, self, radioactivity)
        self.schedule.add(radioactiveWaste)
        self.grid.place_agent(radioactiveWaste, pos)


    def __init__(self, width_zone=10, height=20, initial_robots=10, initial_wastes=20):

        super().__init__()
        
        """Set parameters. Width, robots and wastes given by the server is always multiplied by three.
        Because width is divided in three zones, wastes in three colors and robots also in three colors."""  
        
        self.width = width_zone * 3
        self.height = height
        self.initial_robots = initial_robots
        self.initial_wastes = initial_wastes
        self.totalBadWaste = initial_wastes*3

        self.zone1 = (0,width_zone-1)
        self.zone2 = (width_zone-1,width_zone*2-1)
        self.zone3 = (width_zone*2-1,width_zone*3)

        # Scheduler and message service initialization.
        self.schedule = RandomActivationByTypeFiltered(self)
        self.__messages_service = MessageService(self.schedule)
        MessageService.get_instance().set_instant_delivery(False)
        
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.datacollector = mesa.DataCollector(
            {
                "Waste not processed": "totalBadWaste",
            }
        )

        # Create white robots
        for i in range(self.initial_robots):
            x = self.random.randrange(self.zone1[1])
            y = self.random.randrange(self.height)
            whiteRobots = WhiteRobots(self.next_id(), (x, y), self, (0,self.zone1[1]))
            self.schedule.add(whiteRobots)
            self.grid.place_agent(whiteRobots, (x, y))
        
        # Create yellow robots
        for i in range(self.initial_robots):
            x = self.random.randrange(self.zone2[1])
            y = self.random.randrange(self.height)
            yellowRobots = YellowRobots(self.next_id(), (x, y), self, (0,self.zone2[1]))
            self.schedule.add(yellowRobots)
            self.grid.place_agent(yellowRobots, (x, y))

        # Create red robots
        for i in range(self.initial_robots):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            redRobots = RedRobots(self.next_id(), (x, y), self, (0,self.width))
            self.schedule.add(redRobots)
            self.grid.place_agent(redRobots, (x, y))

        # Create wastes
        for radioactivity in range(3):
            for i in range(self.initial_wastes):
                if radioactivity == 0:
                    x = self.random.randrange(self.zone1[1])
                    y = self.random.randrange(self.height)
                elif radioactivity == 1:
                    x = self.random.randrange(self.zone2[1])
                    y = self.random.randrange(self.height)
                else:
                    x = self.random.randrange(self.width)
                    y = self.random.randrange(self.height)

                radioactiveWaste = RadioactiveWaste(self.next_id(), (x, y), self, radioactivity)
                self.schedule.add(radioactiveWaste)
                self.grid.place_agent(radioactiveWaste, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.__messages_service.dispatch_messages()

        self.totalBadWaste = 0
        for agent in self.schedule.agents:
            if isinstance(agent, RadioactiveWaste):
                if not (agent.pos[0] == self.zone3[1] - 1 and agent.radioactivity == 2):
                    self.totalBadWaste += 1
            elif isinstance(agent, Robot):
                if(Robot.inventory >= 2):
                    self.totalBadWaste += Robot.inventory

        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):

        for i in range(step_count):
            self.step()