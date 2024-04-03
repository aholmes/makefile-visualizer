#!/usr/bin/python

import sys
import json
import random


class Id(object):

    def __init__(self):
        super().__init__()
        self._i = 0

    @property
    def i(self):
        self._i += 1
        return self._i

def random_hex():
    r = lambda: random.randint(0,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))

def main(args):
    _parse_args(args)

    i = Id()
    print("@startuml")
    print("""left to right direction
skinparam artifact {
  BackgroundColor<<FILLED>> gray
}
skinparam linetype ortho
skinparam Arrow {
Thickness .5
Color Black
}
skinparam nodesep 10
skinparam ranksep 1""")
    for graph in json.load(sys.stdin):
        print_single_graph(graph, i)
    print("@enduml")


def print_single_graph(graph, i):
    name_to_node = {}
    print("component {")

    parents = []
    for target, deps in graph.items():
        target_str = _escape(target)
        parents.append(target_str)
   
    for target, deps in graph.items():
        target_color = random_hex()
        target_str = _escape(target)
        _register_node(target_str, i, name_to_node, target_color)
        target_node = name_to_node[target_str]
        for dep_str in (_escape(dep) for dep in deps):
            if dep_str in parents:
                _register_node(dep_str, i, name_to_node, target_color)
            else:
                _register_filled_node(dep_str, i)
            print('{} <-- {} {}'.format(target_node, name_to_node[dep_str], target_color))
    print("}")

def _register_node(name, i, name_to_node, target_color, fill_opacity=30):
    if not (name in name_to_node):
        node = 'n{}'.format(i.i)
        name_to_node[name] = node
        print('artifact {} as {} {}{}'.format(name.replace('__', '~__'), node.replace('__', '~__'), target_color, fill_opacity))
        
def _register_filled_node(name, i, name_to_node):
    if not (name in name_to_node):
        node = 'n{}'.format(i.i)
        name_to_node[name] = node
        print('artifact {} as {} <<FILLED>>'.format(name, node))

def _escape(s):
    return '"{}"'.format(s.replace('"', r'\"').replace('#', ''))


def _parse_args(args):
    if len(args) != 1:
        print('# convert a dependency graph stored in JSON format to PUML format')
        print('{} < deps.json | plantuml -tsvg -p >| makefile.svg'.format(args[0]))
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
