from bots.btnode import BTNode
from replay import *
import numpy as np


class DistanceFromOpponent(BTNode):
    def parseArgs(self, args):
        if len(args) > 0:
            self.id = args[0]
            # 0:Red and 1:Blue Look in replay.py
            self.team = args[1]
            self.dist = args[2]

    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            game = gameworld.game
            player = [
                game_player
                for game_player in game.players
                if game_player.team == self.team
            ][0]
            opponent_player = [
                game_player
                for game_player in game.players
                if not game_player.team == self.team
            ][0]

            # TODO: Modify it for 2v2 or 3v3 case.

            # ball_loc = np.array([game.ball.x, game.ball.y])
            player_loc = np.array([player.disc.x, player.disc.y])
            opponent_player_loc= np.array([opponent_player.disc.x, opponent_player.disc.y])
            # player_dist = np.linalg.norm(player_loc - ball_loc)
            opponent_player_dist = np.linalg.norm(opponent_player_loc - player_loc)
            if opponent_player_dist < self.dist:
                return True
            return False
        return None
