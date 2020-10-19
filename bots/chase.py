from bots.btnode import BTNode
import replay

class Chase(BTNode):
    def execute(self):
        BTNode.execute(self)
        gameworld = self.agent
        if gameworld.player:
            t = 0
            px = gameworld.player.disc.x
            py = gameworld.player.disc.y

            bx = gameworld.game.ball.x
            by = gameworld.game.ball.y

            inputs = []
            if abs(px - bx) > t:
                inputs.append(replay.Input.Right if px < bx else replay.Input.Left)

            if abs(py - by) > t:
                inputs.append(replay.Input.Down if py < by else replay.Input.Up)

            gameworld.setInput(*inputs)
            return None
        return True
