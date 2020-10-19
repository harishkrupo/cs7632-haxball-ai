import replay
from bots import interactive
import inspect

class BehaviourTree(interactive.Interactive):
    def buildTree(self, spec):
        self.root = buildTreeAux(spec, self)

    def onUpdate(self):
        res = self.root.execute()
        if res is not None:
            self.root.reset()
        return res


### Parse the behavior tree symbolic specification
def buildTreeAux(spec, agent):
    # If you see a symbol, make the node without arguments
    if not isinstance(spec, tuple) and inspect.isclass(spec):
        n = spec(agent)
        return n
    # If you see a tuple, make the node with type in the first position, and pass in the rest of the tuple as arguments
    elif isinstance(spec, tuple) and len(spec) > 0 and inspect.isclass(spec[0]):
        first, rest = spec[0], spec[1:]
        n = first(agent, rest)
        return n
    # If you see a list, recursively build the tree. First element is root of subtree and rest are children of the root
    elif isinstance(spec, list) and len(spec) > 0:
        first, rest = spec[0], spec[1:]
        n = buildTreeAux(first, agent)
        for r in rest:
            child = buildTreeAux(r, agent)
            n.addChild(child)
        return n
