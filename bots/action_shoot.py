from bots.btnode import BTNode
from replay import *

class Shoot(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            inputs = []
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            xdiff = abs(px - bx)
            ydiff = abs(py - by)

            ret = True
            xproximity = xdiff > 40
            yproximity = ydiff > 40
            if xproximity:
                inputs.append(Input.Right if px < bx else Input.Left)
                ret = False

            if yproximity:
                inputs.append(Input.Down if py < by else Input.Up)
                ret = False

            if ret:
                inputs.append(Input.Kick)

            gameworld.setInput(*inputs)
            return True
        return None

