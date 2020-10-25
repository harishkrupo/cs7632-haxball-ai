from bots.btnode import BTNode
from replay import *

class Shoot(BTNode):
    def execute(self):
        print("Shoooooooooooooooting")
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            inputs = []
            inputs.append(Input.Kick)
            print("Shoooooooooooooooting")
            gameworld.setInput(*inputs)
            return True
        return None

