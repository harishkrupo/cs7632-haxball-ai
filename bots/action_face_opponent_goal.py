from bots.btnode import BTNode
from replay import *
from bots.constants import *
from bots.utils import *


class FaceOpponentGoal(BTNode):
    def execute(self, delta=0):
        BTNode.execute(self)
        gameworld = self.agent

        if gameworld.player:
            inputs = []
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            enemy_goal_x = -370 if gameworld.player.team == Team.Blue else 370
            enemy_goal_y_top = -55
            enemy_goal_y_bottom = 55
            enemy_goal_y_middle = (enemy_goal_y_top + enemy_goal_y_bottom) / 2
            
            ball_distance = distance((bx, by), (enemy_goal_x, enemy_goal_y_middle))
            player_distance = distance((px, py), (enemy_goal_x, enemy_goal_y_middle))

            if ball_distance > player_distance:
                lw_dist = dist_point_from_line(locations["tlc"], locations["blc"], (px, py))

                if lw_dist > bot_size:
                    inputs.append(Input.Left)
                else:
                    inputs.append(Input.Right)

                inputs.append(Input.Down)
            else:
                _, y = point_of_intersection(
                    (bx, by),
                    (px, py),
                    (enemy_goal_x, enemy_goal_y_top),
                    (enemy_goal_x, enemy_goal_y_bottom)
                )

                if y < enemy_goal_y_top:
                    inputs.append(Input.Left)
                elif y > enemy_goal_y_bottom:
                    inputs.append(Input.Right)

            gameworld.setInput(*inputs)
            return True
        return None
