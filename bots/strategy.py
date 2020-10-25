from bots.chase import Chase
from bots.shoot import Shoot
from bots.sequence_and_selector import Sequence, Selector

class Strategy():
    def __init__(self):
        self.spec = [(Sequence, "sequence"), (Chase, "Chaser"), (Shoot, "Shooter")]

    def getStrategy(self):
        return self.spec
