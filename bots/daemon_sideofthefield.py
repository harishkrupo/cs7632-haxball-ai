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
