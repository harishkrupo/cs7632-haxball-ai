from bots.btnode import BTNode
from replay import *
from bots.constants import locations
import numpy as np

class Align(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            rtg = locations["rtg"]
            rbg = locations["rbg"]

            ball_top_goal_vector = [rtg[0] - bx, rtg[1] - by]
            ball_bottom_goal_vector = [rbg[0] - bx, rbg[1] - by]
            player_ball_vector = [px - bx, py - by]

            pbv_btg = np.cross(player_ball_vector, ball_top_goal_vector) > 0
            pbv_bbg = np.cross(player_ball_vector, ball_bottom_goal_vector) > 0

            inputs = []

            print(pbv_btg, pbv_bbg)
            ret = True
            if not (rtg[0] < bx < px):
                inputs.append(Input.Right)
                ret = False

            if pbv_btg and pbv_bbg:
                inputs.append(Input.Up)
                ret = False
            elif (not pbv_btg) and (not pbv_bbg):
                inputs.append(Input.Down)
                ret = False

            gameworld.setInput(*inputs)
            return ret
        return None

