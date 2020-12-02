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
from bots.utils import *

class DefenderChase(BTNode):
    def parseArgs(self, args):
        if len(args) > 0:
            self.clear_distance = args[0]

        if len(args) > 1:
            self.id = args[1]

    def enter(self):
        self.current_kick_count = 0
        self.interval_between_kicks = 100 - 100 * self.agent.get_difficulty()

    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            if self.current_kick_count >= self.interval_between_kicks:
                self.current_kick_count = -1
            self.current_kick_count += 1

            t = 36
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            if gameworld.player.team == replay.Team.Blue:
                goal_top = locations["rtg"]
                goal_bottom = locations["rbg"]
                self_goal_middle = locations["btg"][0], (locations["btg"][1] + locations["bbg"][1]) / 2
            else:
                goal_top = locations["btg"]
                goal_bottom = locations["bbg"]
                self_goal_middle = locations["rtg"][0], (locations["rtg"][1] + locations["rbg"][1]) / 2

            if distance(self_goal_middle, (bx, by)) > self.clear_distance:
                return False

            xdiff = abs(px - bx)
            ydiff = abs(py - by)
            dist = np.sqrt(xdiff ** 2 + ydiff ** 2)

            ball_top_goal_vector = [goal_top[0] - bx, goal_top[1] - by]
            ball_bottom_goal_vector = [goal_bottom[0] - bx, goal_bottom[1] - by]
            player_ball_vector = [px - bx, py - by]
            playerball_cross_topgoalball = np.cross(
                player_ball_vector, ball_top_goal_vector
            )
            playerball_cross_bottomgoalball = np.cross(
                player_ball_vector, ball_bottom_goal_vector
            )
            if gameworld.player.team == replay.Team.Blue:
                playerball_cross_topgoalball = playerball_cross_topgoalball > 0
                playerball_cross_bottomgoalball = playerball_cross_bottomgoalball > 0
            else:
                playerball_cross_topgoalball = playerball_cross_topgoalball < 0
                playerball_cross_bottomgoalball = playerball_cross_bottomgoalball < 0

            inputs = []
            if dist < t:
                if gameworld.player.team == replay.Team.Blue:
                    if (goal_top[0] < bx < px) and (
                        playerball_cross_bottomgoalball != playerball_cross_topgoalball
                    ):
                        if self.current_kick_count <= 0:
                            inputs.append(replay.Input.Kick)

                elif gameworld.player.team == replay.Team.Red:
                    if (goal_top[0] > bx > px) and (
                        playerball_cross_bottomgoalball != playerball_cross_topgoalball
                    ):
                        if self.current_kick_count <= 0:
                            inputs.append(replay.Input.Kick)

                gameworld.setInput(*inputs)
                return True
            xproximity = xdiff > 10
            yproximity = ydiff > 10

            if xproximity:
                inputs.append(replay.Input.Right if px < bx else replay.Input.Left)

            if yproximity:
                inputs.append(replay.Input.Down if py < by else replay.Input.Up)

            gameworld.setInput(*inputs)
            return None
        return False
