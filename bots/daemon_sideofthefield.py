import replay
from bots.btnode import BTNode


class SideOfTheFieldDaemon(BTNode):
    def execute(self, delta=0):
        BTNode.execute(self)
        player = self.agent.player

        if player:
            # player's x coordinate
            px = player.disc.x

            if player.team == replay.Team.Red:
                if px > 0 and len(self.children) > 0:
                    self.children[0].execute()
                    return True
                else:
                    return False
            else:
                if px < 0 and len(self.children) > 1:
                    self.children[1].execute()
                    return True
                else:
                    return False

        return True
