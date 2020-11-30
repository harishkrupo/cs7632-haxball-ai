import replay
from bots.btnode import BTNode
from bots.constants import locations
from bots.utils import distance, point_of_intersection
import random


class DangerToGoal(BTNode):
    """
    Function to check if the defender bot should aline along line of the opponent and the ball
    so that it can block the shoot from the opponent
        1. Find the opponent that is closest to the ball
        2. Check if they form a direct line inside self goal, if yes, return true else false
    """
    def parseArgs(self, args):
        if len(args) > 0:
            self.clear_distance = args[0]

        if len(args) > 1:
            self.id = args[1]

    def execute(self):
        BTNode.execute(self)
        player = self.agent.player
        gameworld = self.agent
        game = self.agent.game
        ball = game.ball

        if player:

            ball_pos = ball.x, ball.y

            self_goal_post_top = locations['rtg'] if player.team == replay.Team.Red else locations['btg']
            self_goal_post_bottom = locations['rbg'] if player.team == replay.Team.Red else locations['bbg']

            goal_middle_pos = (self_goal_post_top[0], (self_goal_post_top[1] + self_goal_post_bottom[1]) / 2)

            r = random.random()

            if distance(goal_middle_pos, ball_pos) < self.clear_distance and r < gameworld.get_difficulty():
                return True

            return False
        return None
