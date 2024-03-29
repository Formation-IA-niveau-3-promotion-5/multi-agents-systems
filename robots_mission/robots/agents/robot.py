"""
Generalized behavior for random walking, one grid cell at a time.
"""

from .communicating import CommunicatingAgent

class Robot(CommunicatingAgent):
    """
    Class implementing random walker methods in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    inventory = 0

    grid = None
    x = None
    y = None
    moore = True

    def __init__(self, unique_id, pos, model, moore=True):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        limit: Robots grid limitations on x plan needs to be a tuple with (min, max).
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self, limit):
        """
        Step one cell in any allowable direction.
        Robots cannot move on another occupied cell. It's working because all robots step asynchronously.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        available_moves = []
        for move in next_moves:
            if self.check_is_cell_available(move) and max(0, limit[0]) <= move[0] <= limit[1]:
                available_moves.append(move)

        if len(available_moves) > 0:
            next_move = self.random.choice(available_moves)
            self.model.grid.move_agent(self, next_move)

    def check_is_cell_available(self, cell):
        """
        Function to check if a cell is available, meaning it doesn't contains any robots.
        Return False when one robot or more is on the cell, else True.
        """
        cell_content = self.model.grid.get_cell_list_contents(cell)
        robots = [obj for obj in cell_content if isinstance(obj, Robot)]
        if len(robots) > 0:
            return False
        else:
            return True
