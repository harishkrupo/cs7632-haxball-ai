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


class MoveCloseToOpponent(BTNode):
    """
    This is the precursor of 'slightly deviate' but can work independently too
    Simple logic: locate the opponent, approach the opponent, return true when in a given range of opponent
    Complex logic that can be incorporated later:
        Somehow consider the location of the ball as well and 'smart approach' the opponent
    """

    def execute(self):
        BTNode.execute(self)
        player = self.agent.player
        game = self.agent.game
        enemy_player = [game_player for game_player in game.players if not game_player.team == player.team][
            0] if game.players else None

        if player and enemy_player:
            # TODO: calibrate
            distance_to_true = 98

            player_pos = (player.disc.x, player.disc.y)
            enemy_player_pos = (enemy_player.disc.x, enemy_player.disc.y)

            # TODO: scale for 2v2 and 3v3
            xdiff = abs(player_pos[0] - enemy_player_pos[0])
            ydiff = abs(player_pos[1] - enemy_player_pos[1])
            dist_btw_players = np.sqrt(xdiff ** 2 + ydiff ** 2)

            inputs = []
            # Here it will always be possible to reach near the opponent player, thus we do not return false explicitly
            if dist_btw_players <= distance_to_true:
                return True

            if xdiff > 0:
                inputs.append(replay.Input.Right if player_pos[0] < enemy_player_pos[0] else replay.Input.Left)
            if ydiff > 0:
                inputs.append(replay.Input.Down if player_pos[1] < enemy_player_pos[1] else replay.Input.Up)

            self.agent.setInput(*inputs)
            return None
        return False
