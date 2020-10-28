from bots.btnode import BTNode
from replay import *
import numpy as np


class ClosestTeamToBall(BTNode):
    def parseArgs(self, args):
        if len(args) > 0:
            self.id = args[0]
            # 0:Red and 1:Blue Look in replay.py
            self.team = args[1]

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

            ball_loc = np.array([game.ball.x, game.ball.y])
            player_loc = np.array([player.disc.x, player.disc.y])
            opponent_player_loc= np.array([opponent_player.disc.x, opponent_player.disc.y])
            player_dist = np.linalg.norm(player_loc - ball_loc)
            opponent_player_dist = np.linalg.norm(opponent_player_loc - ball_loc)

            if player_dist < opponent_player_dist:
                print("Given Team: {} is closer to ball".format(self.team))
                return True
            return False
        return None
