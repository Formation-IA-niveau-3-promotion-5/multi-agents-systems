from .robot import Robot
from robots.message.MessagePerformative import MessagePerformative

# All robots type, to be completed with particular behaviors...
class WhiteRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 0
        super().__init__(unique_id, pos, model)

    def step(self):
        self.random_move(self.limit)

class YellowRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 1
        super().__init__(unique_id, pos, model)

    def step(self):
        self.random_move(self.limit)

class RedRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 2
        super().__init__(unique_id, pos, model)

    def step(self):
        self.random_move(self.limit)