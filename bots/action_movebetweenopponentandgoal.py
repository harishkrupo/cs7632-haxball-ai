from bots.btnode import BTNode
import replay

class MoveBetweenOpponentAndGoal(BTNode):
	# on defense, we want to make sure our player is in a good position to intercept the ball
	# assuming the enemy player has the ball, we want our player to be between the ball and the goal
	# as such, tell the player to be a certain percent of the way between the ball and the middle of the goal
	# for example, if self.percentage = 0.75, the ball is at (2, 0), and the middle of our goal is at (370, 0), we should tell the player to move to (278, 0)

	def parseArgs(self, args):
		if len(args) > 1:
			self.id = args[0]
			self.percentage = args[1]
		else:
			self.percentage = args[0]

	def execute(self, delta = 0):
		BTNode.execute(self)
		player = self.agent.player
		game = self.agent.game
		ball = game.ball
		enemy_player = [game_player for game_player in game.players if not game_player.team == player.team][0] if game.players else None

		if player and enemy_player:
			# our goal's coordinates
			our_goal_x = 370 if player.team == replay.Team.Blue else -370
			our_goal_y_top = -55
			our_goal_y_bottom = 55
			our_goal_y_middle = (our_goal_y_top + our_goal_y_bottom) / 2

			# player's coordinates
			px = player.disc.x
			py = player.disc.y

			# ball's coordinates
			bx = ball.x
			by = ball.y

			# destination coordinates -- this is where we want to move the player so they're ready on defense
			destination_x = bx - abs(bx - our_goal_x) * self.percentage if player.team == replay.Team.Red else bx + abs(bx - our_goal_x) * self.percentage
			destination_y = by - abs(by - our_goal_y_middle) * self.percentage if by > 0 else by + abs(by - our_goal_y_middle) * self.percentage

			inputs = []
			# move the player horizontally to the destination
			if px > destination_x:
				inputs.append(replay.Input.Left)
			elif px < destination_x:
				inputs.append(replay.Input.Right)
			# move the player vertically to the destination
			if py > destination_y: # NOTE: top of the map is negative-y and the bottom of the map is positive-y
				inputs.append(replay.Input.Up)
			elif py < destination_y:
				inputs.append(replay.Input.Down)

			self.agent.setInput(*inputs)
			return None
		return True

def get_destination_coordinate(ball_pos, goal_pos):
	slope = ( ball_pos[1] - goal_pos[1] ) / ( ball_pos[0] - goal_pos[0] ) # calculate slope of line between ball and goal
	extrapolated_point_y = (intersect_point[0] - line_begin[0]) * slope
	return abs(extrapolated_point_y - intersect_point[1]) < 5
