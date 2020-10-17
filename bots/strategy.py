from bots.chase import Chase

class Strategy():
    def __init__(self):
        self.spec = [Chase]

    def getStrategy(self):
        return self.spec
