from bots.btnode import BTNode
from replay import *

class Align(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            inputs = []
            inputs.append(Input.Kick)
            gameworld.setInput(*inputs)
            return True
        return None

