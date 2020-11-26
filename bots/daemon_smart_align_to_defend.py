import replay
from bots.btnode import BTNode
from bots.constants import locations
from bots.utils import distance, point_of_intersection


class SmartAlignToDefend(BTNode):
    """
    Function to check if the defender bot should aline along line of the opponent and the ball
    so that it can block the shoot from the opponent
        1. Find the opponent that is closest to the ball
        2. Check if they form a direct line inside self goal, if yes, return true else false
    """
    def parseArgs(self, args):
        if len(args) > 0:
            self.id = args[0]

    def execute(self):
        BTNode.execute(self)
        player = self.agent.player
        game = self.agent.game
        ball = game.ball

        if player:

            # if the closest opponent is within the given distance of the ball, only then we consider it
            min_dist_for_true = 180

            # get ball pos and the line for self goal
            ball_pos = (ball.x, ball.y)
            self_goal_line = (locations['rtg'], locations['rbg']) if player.team == replay.Team.Red else (locations['btg'], locations['bbg'])

            # get all the opponents
            opp_dist_from_ball = float("inf")
            opponent = None
            for game_player in game.players:
                if game_player.team != player.team:
                    tmp_dist = distance((game_player.disc.x, game_player.disc.y), ball_pos)
                    if tmp_dist < opp_dist_from_ball:
                        opp_dist_from_ball = tmp_dist
                        opponent = game_player

            if opponent:
                opponent_pos = (opponent.disc.x, opponent.disc.y)
                if distance(opponent_pos, ball_pos) > min_dist_for_true:
                    return False

                # calculate the x-dists b/w all entities
                x_dist_ball_goal = abs(self_goal_line[0][0] - ball_pos[0])
                x_dist_opponent_goal = abs(self_goal_line[0][0] - opponent_pos[0])
                # if opponent is behind the ball, charging towards self goal
                if x_dist_ball_goal < x_dist_opponent_goal:
                    _, insec_pt_y = point_of_intersection(self_goal_line[0], self_goal_line[1], ball_pos, opponent_pos)

                    # check if the intersection point's y cord lies in the goal
                    if self_goal_line[0][1] <= insec_pt_y <= self_goal_line[1][1]:
                        return True

            return False
        return None
