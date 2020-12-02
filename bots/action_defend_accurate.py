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
from bots.constants import *
from bots.utils import *
import replay


class DefendAccurate(BTNode):
    # on defense, we want to make sure our player is in a good position to intercept the ball
    # assuming the enemy player has the ball, we want our player to be between the ball and the goal
    # as such, tell the player to be a certain percent of the way between the ball and the middle of the goal
    # for example, if self.percentage = 0.75, the ball is at (2, 0), and the middle of our goal is at (370, 0), we should tell the player to move to (278, 0)

    def parseArgs(self, args):
        self.percentage = args[0]
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta=0):
        BTNode.execute(self)
        player = self.agent.player
        game = self.agent.game
        ball = game.ball
        enemy_players = [game_player for game_player in game.players if not game_player.team == player.team] \
            if game.players else None

        enemy_player = None

        if enemy_players is not None:
            min_distance = float("inf")

            for p in enemy_players:
                if p is None:
                    continue

                player_distance = distance((p.disc.x, p.disc.y), (ball.x, ball.y))

                if player_distance < min_distance:
                    min_distance = player_distance
                    enemy_player = p

        if player and enemy_player:
            # our goal's coordinates
            our_goal_x = locations["btg"][0] if player.team == replay.Team.Blue else locations["rtg"][0]
            our_goal_y_top = locations["btg"][1]
            our_goal_y_bottom = locations["bbg"][1]

            ex = enemy_player.disc.x
            ey = enemy_player.disc.y

            # player's coordinates
            px = player.disc.x
            py = player.disc.y

            # ball's coordinates
            bx = ball.x
            by = ball.y

            bound_top_y = locations["trc"][1]
            bound_bot_y = locations["brc"][1]

            destination_x = bx * (1 - self.percentage) + our_goal_x * self.percentage

            destination_x, destination_y = point_of_intersection(
                (ex, ey),
                (bx, by),
                (destination_x, bound_top_y),
                (destination_x, bound_bot_y)
            )

            # destination_x = locations["btg"][0] - 100 if player.team == replay.Team.Blue else locations["rtg"][0] + 100

            print(player.team == replay.Team.Blue)
            print(destination_x, destination_y)

            # if px - destination_x < 1:
            #     destination_x = px
            #
            # if py - destination_y < 1:
            #     destination_y = py

            # destination coordinates -- this is where we want to move the player so they're ready on defense
            # destination_x = bx - abs(bx - our_goal_x) * self.percentage if player.team == replay.Team.Red else bx + abs(
            #     bx - our_goal_x) * self.percentage
            # destination_y = by - abs(by - our_goal_y_middle) * self.percentage if by > 0 else by + abs(
            #     by - our_goal_y_middle) * self.percentage

            inputs = []
            # move the player horizontally to the destination
            if px > destination_x + 5:
                inputs.append(replay.Input.Left)
            elif px < destination_x - 5:
                inputs.append(replay.Input.Right)
            # move the player vertically to the destination
            if py > destination_y + 5:  # NOTE: top of the map is negative-y and the bottom of the map is positive-y
                inputs.append(replay.Input.Up)
            elif py < destination_y - 5:
                inputs.append(replay.Input.Down)

            self.agent.setInput(*inputs)
            return True
        return True


def get_destination_coordinate(ball_pos, goal_pos):
    slope = (ball_pos[1] - goal_pos[1]) / (ball_pos[0] - goal_pos[0])  # calculate slope of line between ball and goal
    extrapolated_point_y = (intersect_point[0] - line_begin[0]) * slope
    return abs(extrapolated_point_y - intersect_point[1]) < 5
