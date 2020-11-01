from bots.btnode import BTNode
from replay import *
from bots.constants import *
from bots.utils import *


class ShootAtWall(BTNode):
    def execute(self, delta=0):
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

            lw_dist = dist_point_from_line(locations["tlc"], locations["blc"], (bx, by))
            rw_dist = dist_point_from_line(locations["trc"], locations["brc"], (bx, by))

            if lw_dist < rw_dist:
                wall = locations["tlc"], locations["blc"]
            else:
                wall = locations["trc"], locations["brc"]

            if ret:
                angle_with_wall = angle_between_lines((px, py), (bx, by), *wall)

                if 10 < angle_with_wall < 170:
                    inputs.append(Input.Kick)

            gameworld.setInput(*inputs)
            return True
        return None

