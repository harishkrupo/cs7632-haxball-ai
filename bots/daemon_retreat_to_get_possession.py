"""
 * Copyright 2020 cs7632-haxball-ai team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import replay
from bots.btnode import BTNode
from bots.constants import locations


class RetreatToGetPossession(BTNode):
    """
    Simple function that checks if we need to retreat towards our goal to get possession of the ball.
    Current naive logic:
        1. checks if our player lies at half field length + some delta (extra room for calibration). (the logic here
            is that if we are significantly inside the opponents field, we might not want to retreat but instead charge)
        2. checks if the ball lie between the player pos and self goal pos - if yes returns true else false
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
            # TODO: calibrate
            # delta defines the 'strictness' in returning true
            # smaller the delta - less liberty we have - more chance for true if ball lies b/w player and self goal
            delta = 42

            player_pos = (player.disc.x, player.disc.y)
            ball_pos = (ball.x, ball.y)
            self_goal_x = locations['rtg'][0] if player.team == replay.Team.Red else locations['btg'][0]

            # get the mid field length
            half_field = abs(self_goal_x)
            # TODO: calibrate
            # larger the value of field_delta, more the chance that daemon is potentially true
            field_delta = half_field / 4

            # calculate the x-dists b/w all entities
            x_dist_ball_goal = abs(self_goal_x - ball_pos[0])
            x_dist_player_goal = abs(self_goal_x - player_pos[0])

            # check if player is half_field + field_delta distance away from self_post
            if x_dist_player_goal > half_field + field_delta:
                return False

            if x_dist_ball_goal + delta < x_dist_player_goal:
                return True

            return False
        return None
