#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
import sys
from file_gestion import read_file
import generation
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets
from itertools import chain, combinations


def get_max_coherent_set(structure):
    """
    Finds the largest coherent set of ballots
    :param structure: data extracted from an election file
    :return: largest coherent set of ballots
    """
    L=[]
    m=0
    l_set=Set()
    for ballot in structure["preferences"]:
        if isinstance(ballot[1][-1], (long, int)):
            L+=[ballot[1]]
        else:
            L+=[ballot[1][:-1]]
    subsets = list(chain.from_iterable(combinations(L,n) for n in range(len(L)+1)))
    subsets = [[Set(i) for i in j] for j in subsets]
    print subsets
    for s in subsets:
        try:
            Ls = s
            print s
            elements = Set(chain.from_iterable(s))
            Ls += [Set([i]) for i in elements]
            reorder_sets(Ls)
        except ValueError:
            continue
        else:
            if len(s)>=m:
                m=len(s)
                l_set=s
    return m,l_set

if __name__ == '__main__':
    #if len(sys.argv) != 2:
    #    sys.exit("This program takes one and only one argument")
    #filename = sys.argv[1]
    #structure = read_file(filename)
    #print(structure["candidates"])
    #print(structure["preferences"])
    #structure=generation.generation(10,8)
    #str_example={'nb_candidates': 5, 'preferences': [(1, [5, 2, 1, 3, 4, {}]), (1, [5, {1, 2, 3, 4}]), (1, [2, 5, 3, 1, {4}])], 'sum_vote_count': 3, 'candidates': {0: 'Candidate 0', 1: 'Candidate 1', 2: 'Candidate 2', 3: 'Candidate 3', 4: 'Candidate 4', 5: 'Candidate 5'}, 'nb_unique_orders': 3, 'nb_voters': 3}
    str_example2={'nb_candidates': 5, 'preferences': [(1, [5, 3, 2, 4, {1}]), (1, [2, 4, {1, 3, 5}]), (1, [3, 5, 2, 4, {1}])], 'sum_vote_count': 3, 'candidates': {0: 'Candidate 0', 1: 'Candidate 1', 2: 'Candidate 2', 3: 'Candidate 3', 4: 'Candidate 4', 5: 'Candidate 5'}, 'nb_unique_orders': 3, 'nb_voters': 3}
    print str_example2
    size,largest_coherent_set=get_max_coherent_set(str_example2)
    print(size,largest_coherent_set)