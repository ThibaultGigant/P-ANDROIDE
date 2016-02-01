#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
import sys
from file_gestion import read_file
import generation
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
    l_set=set()
    for ballot in structure["preferences"]:
        if isinstance(ballot[1][-1], (long, int)):
            L+=[ballot[1]]
        else:
            L+=[ballot[1][:-1]]
    subsets=list(chain.from_iterable(combinations(L,n) for n in range(len(L)+1)))
    for s in subsets:
        try:
            Ls=list(s)
            elements=set(chain.from_iterable(s))
            Ls.extend([i] for i in list(elements))
            reorder_sets(s)
        except ValueError:
            continue
        else:
            if len(s)>m:
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
    structure=generation.generation(5,3)
    print structure
    size,largest_coherent_set=get_max_coherent_set(structure)
    print(size,largest_coherent_set)