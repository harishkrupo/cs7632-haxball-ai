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

###########################
### Selector
###
### A selector node tries each child in order until one succeeds or they all fail. If any child succeeds, the selector node also succeeds and stops trying children. If all children fail, then the selector node also fails.


class Selector(BTNode):

    ### execute() is called every tick. It recursively tries to execute the currently indexed child.
    ### If the child succeeds, the selector node succeeds and returns True.
    ### If the child fails, the selector goes on to the next child in the next tick. If the selector gets to the end of the list and all children have failed, the selector fails and returns False.
    ### If a child requires several ticks to complete execution, then the child will return None. If a child returns None, the selector also returns None.
    ### If a selector node has no children, it fails.
    def execute(self, delta=0):
        BTNode.execute(self, delta)
        ### YOUR CODE GOES BELOW HERE ###
        if len(self.children) == 0:
            return False

        cIndex = self.getCurrentIndex();
        if cIndex >= len(self.children):
            return False

        childRet = self.children[cIndex].execute()
        if childRet == True:
            self.current = 0;
            return True;

        if childRet == False:
            self.current += 1;
            if self.current >= len(self.children):
                return False;
            else:
                return None;

        if childRet == None:
            return None;

        ### YOUR CODE GOES ABOVE HERE ###
        return False
