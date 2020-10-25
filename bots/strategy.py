from bots.action_chase import Chase
from bots.action_shoot import Shoot
from bots.sequence import Sequence
from bots.selector import Selector
from bots.action_align import Align

class Strategy():
    def __init__(self):
        self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner"), (Shoot, "Shooter")]
        # self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Align, "Aligner")]
        # self.spec = [(Chase, "Chaser")]

    def getStrategy(self):
        return self.spec
