#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from generation import generation
from copy import copy
from sage.all import Set


def bandb(ballots,node,enum_list):
    ballots_bis = copy(ballots)
    while ballots_bis != []:
        b = ballots_bis[0]
        ballots_bis.remove(b)
        node_bis = copy(node)+[b]
        enum_list += [node_bis,copy(node)]
        bandb(ballots_bis,node_bis,enum_list)
    return enum_list

if __name__ == '__main__':
    structure,candidat = generation(5,3,3)
    preferences = structure["preferences"]
    ballots = [couple[1] for couple in preferences]
    # ballot_set = [Set([1,2,3]),Set([2,3]),Set([3,6])]
    print(bandb(ballots,[],[]))
