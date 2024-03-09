import mesa

class RadioactiveWaste(mesa.Agent):
    def __init__(self, unique_id, pos, model, radioactivity):
        """
        RadioactiveWaste is considered as an agent because of the mesa framework limitation.
        Otherwise in others multi-agents languages it would be considered as an item.
        pos: The agent's current x and y coordinates.
        radioactivity: The agent's radioactivity level. Only robots of the same level can pickup this waste.
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.radioactivity = radioactivity

    def step(self):
        pass