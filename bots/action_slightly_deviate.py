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
from bots.constants import *
from bots.utils import *


class SlightlyDeviate(BTNode):
    def execute(self, delta=0):
        BTNode.execute(self)
        gameworld = self.agent

        if gameworld.player:
            inputs = []

            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            lw_dist = dist_point_from_line(locations["tlc"], locations["blc"], (px, py))

            if lw_dist > bot_size:
                inputs.append(Input.Left)
            else:
                inputs.append(Input.Right)

            gameworld.setInput(*inputs)
            return True
        return None
