"""
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
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

import inspect
import replay
from bots import interactive

###########################
### gensym

GENSYMBOL = "g"
GENCOUNT = 0


def gensym():
    global GENCOUNT
    GENCOUNT = GENCOUNT + 1
    return str(GENSYMBOL) + str(GENCOUNT)

###########################
### BTNode
###
### Each update, the execute at the root of the tree will be called, and it recursively figures out which leaf should execute


class BTNode(object):

    ### children: children BTNodes
    ### id: an id number. Randomly assigned unless set.
    ### current: the current child (index integer)
    ### agent: the executing agent
    ### first: is this the first time it is executed?

    def __init__(self, agent, args=[]):
        self.id = gensym()
        self.agent = agent
        self.children = []
        self.current = None
        self.first = True
        self.parseArgs(args)

    def parseArgs(self, args):
        if len(args) > 0:
            self.id = args

    ### Add a child to the BTNode, reset the current counter
    def addChild(self, child):
        self.children.append(child)
        if self.current == None:
            self.current = 0

    ### Perform a behavior, should be called every tick
    ### Returns True if the behavior succeeds, False if the behavior fails, or None if the behavior should continue to execute during the next tick.
    def execute(self, delta=0):
        print("execute", self.id)
        if self.first:
            self.enter()
            self.first = False
        return True

    def enter(self):
        print("enter", self.id)
        return None

    ### Print each node id in tree in a depth-first fashion
    def printTree(self):
        print((type(self), self.id))
        for child in self.children:
            child.printTree()

    ### Reset the tree for another run. For BTNode, this means moving the current child counter back to 0.
    def reset(self):
        self.current = 0
        self.first = True
        for child in self.children:
            child.reset()

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id

    def getAgent(self):
        return self.agent

    def getChild(self, index):
        return self.children[index]

    def getChildren(self):
        return self.children

    def getNumChildren(self):
        return len(self.children)

    def getCurrentIndex(self):
        return self.current

    def setCurrentIndex(self, index):
        self.current = index
