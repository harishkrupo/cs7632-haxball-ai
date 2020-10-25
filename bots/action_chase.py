from bots.btnode import BTNode
import replay
import numpy as np

class Chase(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            t = 36
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            xdiff = abs(px - bx)
            ydiff = abs(py - by)
            dist = np.sqrt(xdiff ** 2 + ydiff ** 2)

            inputs = []
            if dist < t:
                return True

            xproximity = xdiff > 0
            yproximity = ydiff > 0
            if xproximity:
                inputs.append(replay.Input.Right if px < bx else replay.Input.Left)

            if yproximity:
                inputs.append(replay.Input.Down if py < by else replay.Input.Up)

            gameworld.setInput(*inputs)
            return None
        return False
