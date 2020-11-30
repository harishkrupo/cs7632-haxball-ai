from bots.btnode import BTNode
from replay import *

class JustShoot(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            inputs = [Input.Kick]
            gameworld.setInput(*inputs)
            return True
        return None

