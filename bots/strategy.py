from bots.action_chase import Chase
from bots.action_shoot import Shoot
from bots.sequence import Sequence
from bots.selector import Selector
from bots.action_align import Align
from bots.daemon_clearpathtogoal import ClearPathToGoalDaemon
from bots.daemon_sideofthefield import SideOfTheFieldDaemon
from bots.action_movetoopponentside import MoveToOpponentSideAction
from bots.action_movebetweenopponentandgoal import MoveBetweenOpponentAndGoal


class Strategy():
    def __init__(self):
        self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")]
        # self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner")]
        # self.spec = [(Chase, "Chaser")]
        # self.spec = [MoveToOpponentSideAction] [(MoveBetweenOpponentAndGoal, 0.75)] [MoveToOpponentSideAction] [SideOfTheFieldDaemon] [ClearPathToGoalDaemon] -- EXAMPLE ONLY

    def getStrategy(self):
        return self.spec
