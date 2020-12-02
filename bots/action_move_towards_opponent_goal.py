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

from bots.btnode import BTNode
import replay
import numpy as np

from bots.constants import locations


class MoveTowardsOpponentGoal(BTNode):
    """
    The current implementation assumes that call to MoveTowardsOpponentGoal
    is made only after the player has been aligned with the opponent goal and the ball.
    We also assume that we have the possession of the ball.
    Based on this assumption, the node performs the following action:
    1. determines if the ball has gone far enough for it to not be considered in out possession:
        If yes, then we terminate this action
    2. move the player directly towards the ball, with the following logic:
        Current naive logic: just push the ball in the direction of the goal
    """

    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            player = gameworld.player
            ball = gameworld.game.ball
            t = 36

            # delta gives the buffer - larger the value more 'generous' we are in terms of ball possession
            # TODO: calibrate delta
            delta = 4
            distance_to_false = t + delta

            # TODO: scale for 2v2 and 3v3
            player_pos = (player.disc.x, player.disc.y)
            ball_pos = (ball.x, ball.y)

            xdiff = abs(player_pos[0] - ball_pos[0])
            ydiff = abs(player_pos[1] - ball_pos[1])
            dist = np.sqrt(xdiff ** 2 + ydiff ** 2)

            # get the x-dist of the ball from opponent's goal
            opponent_goal_x = locations['btg'][0] if player.team == replay.Team.Red else locations['rtg'][0]
            ball_to_goal_diff = abs(opponent_goal_x - ball_pos[0])

            inputs = []
            # If player has lost possession of the ball or ball has reached close to goal
            # we return false
            if dist > distance_to_false:
                return False
            if ball_to_goal_diff < 250:
                return True

            if xdiff > 0:
                inputs.append(replay.Input.Right if player_pos[0] < ball_pos[0] else replay.Input.Left)
            if ydiff > 0:
                inputs.append(replay.Input.Down if player_pos[1] < ball_pos[1] else replay.Input.Up)

            gameworld.setInput(*inputs)
            return None
        return False
