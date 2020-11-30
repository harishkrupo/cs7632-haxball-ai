from bots.btnode import BTNode
import replay
import numpy as np

from bots.constants import locations


class MoveMiddleOfGoal(BTNode):
    """
    Simple action that moves the player to the center of it teams goal.
    Potential issues: momentum not properly accounted for -- so if we want to move to a point (x, y), we might overshoot
        Naive solution: If we reach within a particular radius of the destination point, we stop and assume that momentum
            will take us to the destination point
    """

    def execute(self):
        BTNode.execute(self)
        player = self.agent.player

        if player:
            # TODO: calibrate
            delta = 0

            player_pos = (player.disc.x, player.disc.y)
            self_goal_post_top = locations['rtg'] if player.team == replay.Team.Red else locations['btg']
            self_goal_post_bottom = locations['rbg'] if player.team == replay.Team.Red else locations['bbg']

            goal_middle_pos = (self_goal_post_top[0], (self_goal_post_top[1] + self_goal_post_bottom[1]) / 2)
            print(goal_middle_pos)

            xdiff = abs(player_pos[0] - goal_middle_pos[0])
            ydiff = abs(player_pos[1] - goal_middle_pos[1])
            dist = np.sqrt(xdiff ** 2 + ydiff ** 2)

            inputs = []
            # Here it will always be possible to reach near the goal, thus we do not return false explicitly
            if dist <= delta:
                return True

            if xdiff > 0:
                inputs.append(replay.Input.Right if player_pos[0] < goal_middle_pos[0] else replay.Input.Left)
            if ydiff > 0:
                inputs.append(replay.Input.Down if player_pos[1] < goal_middle_pos[1] else replay.Input.Up)

            self.agent.setInput(*inputs)
            if xdiff < 37 and ydiff < 37:
                return True
            else:
                return None
        return False
