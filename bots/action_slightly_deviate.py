from bots.btnode import BTNode
from replay import *
from bots.constants import *
from bots.utils import *


class SlightlyDeviate(BTNode):
    def execute(self, delta=0):
        BTNode.execute(self)
        gameworld = self.agent

        if gameworld.player:
            inputs = []

            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            lw_dist = dist_point_from_line(locations["tlc"], locations["blc"], (px, py))

            if lw_dist > bot_size:
                inputs.append(Input.Left)
            else:
                inputs.append(Input.Right)

            gameworld.setInput(*inputs)
            return True
        return None
