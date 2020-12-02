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
from replay import *
import numpy as np


class BallPossession(BTNode):
    def parseArgs(self, args):
        if len(args) > 0:
            self.id = args[0]
            # 0:Red and 1:Blue Look in replay.py
            self.team = args[1]
            self.is_mine = args[2]

    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            t = 90
            player = gameworld.player
            game = gameworld.game
            pteam = player.team
            bx = game.ball.x
            by = game.ball.y

            if self.is_mine:
                px = player.disc.x
                py = player.disc.y
                xdiff = abs(px - bx)
                ydiff = abs(py - by)
                dist = np.sqrt(xdiff ** 2 + ydiff ** 2)
                if pteam == self.team and dist < t:
                    print("OUR TEAM POSSESSION")
                    return True
            else:
                enemy_player = [
                    game_player
                    for game_player in game.players
                    if not game_player.team == player.team
                ][0]
                px = enemy_player.disc.x
                py = enemy_player.disc.y
                xdiff = abs(px - bx)
                ydiff = abs(py - by)
                dist = np.sqrt(xdiff ** 2 + ydiff ** 2)
                if pteam != self.team and dist < t:
                    print("ENEMY TEAM POSSESSION")
                    return True

            return False
        return None
