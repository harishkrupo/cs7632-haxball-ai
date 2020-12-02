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

class SideOfTheFieldDaemon(BTNode):
	def parseArgs(self, args):
		if len(args) > 0:
			self.is_our_team = args[0]
			if len(args) > 1:
				self.id = args[1]

	def execute(self, delta = 0):
		BTNode.execute(self)
		game = self.agent.game
		our_player_team = self.agent.player.team
		player = self.agent.player if self.is_our_team else [game_player for game_player in game.players if not game_player.team == our_player_team][0]

		if player:
			# player's x coordinate
			px = player.disc.x

			if player.team == replay.Team.Red and px > 0:
				return True

			if player.team == replay.Team.Blue and px < 0:
				return True

			return False
		return False
