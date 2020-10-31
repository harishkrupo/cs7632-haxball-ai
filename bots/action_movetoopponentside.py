from bots.btnode import BTNode
import replay
import time

BALL_RADIUS = 10
PLAYER_RADIUS = 15

class MoveToOpponentSideAction(BTNode):
	def execute(self, delta = 0):
		BTNode.execute(self)
		player = self.agent.player
		game = self.agent.game
		ball = game.ball

		if player:
			# enemy goal coordinates
			enemy_goal_x = -370 if player.team == replay.Team.Blue else 370
			enemy_goal_y_top = -55
			enemy_goal_y_bottom = 55
			enemy_goal_y_middle = (enemy_goal_y_top + enemy_goal_y_bottom) / 2

			# player's coordinates
			px = player.disc.x
			py = player.disc.y

			# ball's coordinates
			bx = ball.x
			by = ball.y

			inputs = []
			if player.team == replay.Team.Red:
				print(self.agent.input)
				#print("px {}, bx {}, abs(py - by) {}, margin {}".format(px, bx, abs(py - by), BALL_RADIUS + PLAYER_RADIUS))
				if px < bx and abs(py - by) < BALL_RADIUS + PLAYER_RADIUS - 15: # let's push the ball right so we can get to the opponent's side of the field
					inputs.append(replay.Input.Right)
					print("right1")
				# If we're on the wrong side of the ball, we need to backtrack to get on the left side of the ball, so go Left,
				# BUT make sure we're far enough above or below the ball that we won't start hitting it closer to our goal.
				elif px >= bx - PLAYER_RADIUS - BALL_RADIUS + 10 and abs(py - by) > BALL_RADIUS + PLAYER_RADIUS:
					inputs.append(replay.Input.Left)
					print("left1")
				# If we're on the wrong side of the ball, we need to backtrack to get on the left side of the ball, so we need to go Left,
				# BUT we're too close to the ball (vertically), so we need to move out of the way to prevent hitting it closer to our goal.
				elif px > bx and abs(py - by) <= BALL_RADIUS + PLAYER_RADIUS:
					if py <= by:
						inputs.append(replay.Input.Up) # If we're above the ball, move slightly up and THEN we'll come back and move left.
						print("up2")
					else:
						inputs.append(replay.Input.Down) # If we're below the ball, move slightly down and then we'll come back and move Left.
						print("down2")
				if py < by - 5 and abs(py - by) > BALL_RADIUS and bx - px > BALL_RADIUS + PLAYER_RADIUS: # above the ball AND on the left side of the ball
					inputs.append(replay.Input.Down)
					print("down1")
					if abs(py - by) < BALL_RADIUS + PLAYER_RADIUS + 5:
						inputs.append(replay.Input.Right)
						print("right2")
				elif py > by + 5 and abs(py - by) > BALL_RADIUS and bx - px > BALL_RADIUS + PLAYER_RADIUS: # below the ball AND on the left side of the ball
					inputs.append(replay.Input.Up)
					print("up1")
					if abs(py - by) < BALL_RADIUS + PLAYER_RADIUS + 5:
						inputs.append(replay.Input.Right)
						print("right3")
			elif player.team == replay.Team.Blue:
				print(self.agent.input)
				#print("px {}, bx {}, abs(py - by) {}, margin {}".format(px, bx, abs(py - by), BALL_RADIUS + PLAYER_RADIUS))
				if px > bx and abs(py - by) < BALL_RADIUS + PLAYER_RADIUS - 15: # let's push the ball right so we can get to the opponent's side of the field
					inputs.append(replay.Input.Left)
					print("left1")
				# If we're on the wrong side of the ball, we need to backtrack to get on the left side of the ball, so go Left,
				# BUT make sure we're far enough above or below the ball that we won't start hitting it closer to our goal.
				elif px <= bx - PLAYER_RADIUS - BALL_RADIUS + 10 and abs(py - by) > BALL_RADIUS + PLAYER_RADIUS:
					inputs.append(replay.Input.Right)
					print("right1")
				# If we're on the wrong side of the ball, we need to backtrack to get on the left side of the ball, so we need to go Left,
				# BUT we're too close to the ball (vertically), so we need to move out of the way to prevent hitting it closer to our goal.
				elif px < bx and abs(py - by) <= BALL_RADIUS + PLAYER_RADIUS:
					if py <= by:
						inputs.append(replay.Input.Up) # If we're above the ball, move slightly up and THEN we'll come back and move left.
						print("up2")
					else:
						inputs.append(replay.Input.Down) # If we're below the ball, move slightly down and then we'll come back and move Left.
						print("down2")
				if py < by - 5 and abs(py - by) > BALL_RADIUS and px - bx > BALL_RADIUS + PLAYER_RADIUS: # above the ball AND on the right side of the ball
					inputs.append(replay.Input.Down)
					print("down1")
					if abs(py - by) < BALL_RADIUS + PLAYER_RADIUS + 5:
						inputs.append(replay.Input.Left)
						print("left2")
				elif py > by + 5 and abs(py - by) > BALL_RADIUS and px - bx > BALL_RADIUS + PLAYER_RADIUS: # below the ball AND on the right side of the ball
					inputs.append(replay.Input.Up)
					print("up1")
					if abs(py - by) < BALL_RADIUS + PLAYER_RADIUS + 5:
						inputs.append(replay.Input.Left)
						print("left3")

			'''if abs(px - bx) > abs(py - by): # we are further away on x coordinates, make sure we move closer to the ball
				if player.team == replay.Team.Red:
					if px >= bx:
						inputs.append(replay.Input.Left)
					else:
						inputs.append(replay.Input.Right)
				if player.team == replay.Team.Red:
					if px >= bx:
						inputs.append(replay.Input.Left)
					else:
						inputs.append(replay.Input.Right)
			else: # we are further away on y coordinates
				if py <= by:
					inputs.append(replay.Input.Down)
				else:
					inputs.append(replay.Input.Up)'''

			self.agent.setInput(*inputs)
			return None
		return True
