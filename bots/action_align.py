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
            # get opponents goal loaction
            if gameworld.player.team == Team.Blue:
                goal_top = locations["rtg"]
                goal_bottom = locations["rbg"]
            else:
                goal_top = locations["btg"]
                goal_bottom = locations["bbg"]

            goal_half = (goal_top[1] - goal_bottom[1])/2
            goal_top[1] = goal_top[1] - goal_half * (1 - gameworld.get_difficulty())
            goal_bottom[1] = goal_bottom[1] + goal_half * (1 - gameworld.get_difficulty())

            ball_top_goal_vector = [goal_top[0] - bx, goal_top[1] - by]
            ball_bottom_goal_vector = [goal_bottom[0] - bx, goal_bottom[1] - by]
            player_ball_vector = [px - bx, py - by]
            playerball_cross_topgoalball = np.cross(player_ball_vector, ball_top_goal_vector)
            playerball_cross_bottomgoalball = np.cross(player_ball_vector, ball_bottom_goal_vector)
            if gameworld.player.team == Team.Blue:
                playerball_cross_topgoalball = playerball_cross_topgoalball > 0
                playerball_cross_bottomgoalball = playerball_cross_bottomgoalball > 0
            else:
                playerball_cross_topgoalball = playerball_cross_topgoalball < 0
                playerball_cross_bottomgoalball = playerball_cross_bottomgoalball < 0

            inputs = []

            ret = True
            if gameworld.player.team == Team.Blue:
                if not (goal_top[0] < bx < px):
                    inputs.append(Input.Right)
                    ret = False
            elif gameworld.player.team == Team.Red:
                if not (goal_top[0] > bx > px):
                    inputs.append(Input.Left)
                    ret = False
            elif playerball_cross_topgoalball and playerball_cross_bottomgoalball:
                inputs.append(Input.Up)
                ret = False
            elif (not playerball_cross_topgoalball) and (not playerball_cross_bottomgoalball):
                inputs.append(Input.Down)
                ret = False

            gameworld.setInput(*inputs)

            if ret:
                inputs.append(Input.Kick)
                gameworld.setInput(*inputs)
                # print("Align Successful==================================")
            return ret
        return None

