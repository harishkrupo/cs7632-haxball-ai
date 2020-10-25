from bots.btnode import BTNode
import replay

##########################
### Sequence
###
### A sequence node tries to execute every child in order, one after another. It fails if any child fails. It succeeds when all children have succeeded.


class Sequence(BTNode):

    ### execute() is called every tick. It recursively tries to execute the currently indexed child.
    ### If a child fails, the sequence fails and returns False.
    ### If a child succeeds, the sequence goes on to the next child on the next tick. If the sequence gets to the end of the list, with all children succeeding, the sequence succeeds.
    ### If a child requires several ticks to complete execution, then the child will return None. If a child returns None, the sequence also returns None.
    ### If a sequence node has no children, it succeeds automatically.
    def execute(self, delta=0):
        BTNode.execute(self, delta)
        ### YOUR CODE GOES BELOW HERE ###
        if len(self.children) == 0:
            return True

        cIndex = self.getCurrentIndex();
        if cIndex >= len(self.children):
            return True

        childRet = self.children[cIndex].execute()
        if childRet == False:
            self.current = 0;
            return False;
        if childRet == True:
            self.current += 1
            if self.current >= len(self.children):
                return True;
            else:
                return None;
        if childRet == None:
            return None

        ### YOUR CODE GOES ABOVE HERE ###
        return True
