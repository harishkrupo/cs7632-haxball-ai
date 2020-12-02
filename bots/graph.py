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

import inspect
from bots.strategy import Strategy
from subprocess import PIPE, Popen
import errno

GENCOUNT = 0

def gensym():
    global GENCOUNT
    GENCOUNT = GENCOUNT + 1
    return str(GENCOUNT)

class Node:
    def __init__(self, name):
        self.name = gensym()+ " " + name
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def __str__(self):
        return self.name

def buildGraph(spec):
    if not isinstance(spec, tuple) and inspect.isclass(spec):
        n = Node(spec.__name__)
        return n

    elif isinstance(spec, tuple) and len(spec) > 0 and inspect.isclass(spec[0]):
        first, tag, rest = spec[0], spec[1], spec[2:]
        n = Node(first.__name__)
        return n

    elif isinstance(spec, list) and len(spec) > 0:
        first, rest = spec[0], spec[1:]
        n = buildGraph(first)
        for r in rest:
            child = buildGraph(r)
            n.addChild(child)
        return n

def dot(spec):
    indent = "    ";
    root = buildGraph(spec)
    queue = []
    queue.append(root)
    graph ="digraph {\n";
    while queue:
        elm = queue.pop(0)
        name = elm.name
        for c in elm.children:
            cstr = indent + f"\"{name}\" -> \"{c.name}\";\n"
            graph += cstr
            queue.append(c)
    graph += "}\n";
    return graph

if __name__ == "__main__":
    spec = Strategy().getStrategy();
    graph = dot(spec)
    print(graph)
    try:
        p = Popen(["dot", "-Tpng", "-o", "graph.png"], stdin=PIPE)
        p.communicate(input=graph.encode('utf-8'))
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("Graphviz tool not present")
