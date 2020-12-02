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

class Shoot(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            inputs = []
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            xdiff = abs(px - bx)
            ydiff = abs(py - by)

            ret = True
            xproximity = xdiff > 30
            yproximity = ydiff > 30
            if xproximity:
                inputs.append(Input.Kick)
                inputs.append(Input.Right if px < bx else Input.Left)
                ret = False

            if yproximity:
                inputs.append(Input.Kick)
                inputs.append(Input.Down if py < by else Input.Up)
                ret = False

            if ret:
                inputs.append(Input.Kick)

            gameworld.setInput(*inputs)
            return True
        return None

