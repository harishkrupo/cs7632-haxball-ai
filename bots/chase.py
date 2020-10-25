from bots.btnode import BTNode
import replay
import numpy as np

class Chase(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            t = 30
            # print("===========================")
            # print("VX {} VY {}".format(gameworld.player.disc.vx, gameworld.player.disc.vy))
            # print("===========================")
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            xdiff = abs(px - bx)
            ydiff = abs(py - by)
            dist = np.sqrt(xdiff ** 2 + ydiff ** 2)
            # print("px {} py {} bx {} by {} xdiff {} ydiff {} distance {}".format(px, py, bx, by, xdiff, ydiff, dist))
            inputs = []
            xproximity = xdiff > t
            yproximity = ydiff > t
            if xproximity:
                inputs.append(replay.Input.Right if px < bx else replay.Input.Left)

            if yproximity:
                inputs.append(replay.Input.Down if py < by else replay.Input.Up)

            if dist < t:
                # print("close enough to ball, returning True")
                return True

            gameworld.setInput(*inputs)
            return None
        return False
