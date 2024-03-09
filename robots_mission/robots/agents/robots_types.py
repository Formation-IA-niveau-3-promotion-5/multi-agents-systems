from .robot import Robot
from robots.message.MessagePerformative import MessagePerformative

# All robots type, to be completed with particular behaviors...
class WhiteRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 0
        # self.best_neighbor = -1
        # self.can_move = True
        super().__init__(unique_id, pos, model)

    def step(self):
        self.pickup()
        self.drop()
        # if self.inventory % 2 != 0:
        #     list_messages = self.get_new_messages()
        #     for message in list_messages:
        #         if message.get_performative() == MessagePerformative.ASK_WHY:
        #             if isinstance(message.get_content(), int):
        #                 neighbor_id = message.get_content()
        #                 if self.best_neighbor < neighbor_id:
        #                     self.best_neighbor = neighbor_id
        #         elif message.get_performative() == MessagePerformative.PROPOSE:
        #             if isinstance(message.get_content(), int):
        #                 neighbor_id = message.get_content()
        #                 if self.best_neighbor == neighbor_id:
        #                     if self.unique_id < neighbor_id:
        #                         self.inventory -= 1
        #                     else:
        #                         self.inventory += 1
        #     if self.check_neighborhood() > 1:
        #         self.can_move = False
        #         if self.best_neighbor < 0:
        #             self.model.exchange_message(self, MessagePerformative.ASK_WHY)
        #         else:
        #             self.model.exchange_message(self, MessagePerformative.PROPOSE)
        # else:
        #     self.best_neighbor = -1    
        
        # if self.can_move:
        self.random_move(self.limit)

class YellowRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 1
        super().__init__(unique_id, pos, model)

    def step(self):
        self.pickup()
        self.drop()
        self.random_move(self.limit)

class RedRobots(Robot):
    def __init__(self, unique_id, pos, model, limit):
        self.limit = limit
        self.robot_level = 2
        super().__init__(unique_id, pos, model)

    def step(self):
        self.pickup()
        self.drop()
        self.random_move(self.limit)