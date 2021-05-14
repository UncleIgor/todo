#!/usr/bin/env python3

from anytree import Node, RenderTree, Walker,  Resolver

def genetate_tree(todo):
    for i in range(10):
        #print(i)
        new={'id': 10-i, 'content': "task"}        
        todo.insert(i, new)

def main():
    todo=list()
    genetate_tree(todo)
    
    #print(todo)

main()