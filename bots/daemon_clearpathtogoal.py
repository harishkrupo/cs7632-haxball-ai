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

class ClearPathToGoalDaemon(BTNode):
	def execute(self, delta = 0):
		BTNode.execute(self)
		player = self.agent.player
		game = self.agent.game
		ball = game.ball
		enemy_player = [game_player for game_player in game.players if not game_player.team == player.team][0] if game.players else None

		if player and enemy_player:
			# enemy goal coordinates
			enemy_goal_x = -370 if player.team == replay.Team.Blue else 370
			enemy_goal_y_top = -55
			enemy_goal_y_bottom = 55

			# player's coordinates
			px = player.disc.x
			py = player.disc.y

			# enemy's coordinates
			epx = enemy_player.disc.x
			epy = enemy_player.disc.y

			# ball's coordinates
			bx = ball.x
			by = ball.y

			print((bx, by), (epx, epy), enemy_goal_x, enemy_goal_y_top, enemy_goal_y_bottom)
			clear_goal = direct_line_from_ball_to_goal((bx, by), (epx, epy), enemy_goal_x, enemy_goal_y_top, enemy_goal_y_bottom)
			print("clear goal: {}".format(clear_goal))
			if player.team == replay.Team.Red and px > epx and px < bx and abs(px - bx) < 25 and abs(py - by) < 25 and clear_goal and len(self.children) > 0: # player is on a fast break and is close to the ball
				#inputs.append(replay.Input.Kick) TODO: remove
				self.children[0].execute()
			elif player.team == replay.Team.Blue and px < epx and px > bx and abs(px - bx) < 25 and abs(py - by) < 25 and clear_goal and len(self.children) > 1: # player is on a fast break and is close to the ball
				#inputs.append(replay.Input.Kick) TODO: remove
				self.children[1].execute()

			return None
		return True

def point_intersects(line_begin, line_end, intersect_point):
	slope = ( line_end[1] - line_begin[1] ) / ( line_end[0] - line_begin[0] ) # calculate slope of line
	extrapolated_point_y = (intersect_point[0] - line_begin[0]) * slope
	return abs(extrapolated_point_y - intersect_point[1]) < 5

def direct_line_from_ball_to_goal(ball_position, enemy_position, goal_x, goal_top_y, goal_bottom_y):
	for y in range(goal_top_y, goal_bottom_y):
		if point_intersects(ball_position, (goal_x, y), enemy_position): # is the enemy obstructing the goal in any way?
			return False
	return True
