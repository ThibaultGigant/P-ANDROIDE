#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
# import sys
# from file_gestion import read_file
from generation import generation
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets
from itertools import chain, combinations


def get_max_coherent_set(structure):
    """
    Finds the largest coherent set of ballots
    :param structure: data extracted from an election file
    :return: largest coherent set of ballots and its size
    """
    L = []
    m = 0
    l_set = Set()
    for ballot in structure["preferences"]:
        if isinstance(ballot[1][-1], int):
            L.append(Set(ballot[1]))
        else:
            L.append(Set(ballot[1][:-1]))

    # Creation of all subsets combinations: enumeration of all possible subsets
    subsets = chain.from_iterable(combinations(L, n) for n in range(1, len(L) + 1))

    # Creation of a list of singletons that should be added to each subset of ballots, to avoid problems
    singletons = [Set([i]) for i in structure["candidates"].keys()]

    # Testing each subset to see if it's coherent ==> recuperation of the largest subset
    for subset in subsets:
        try:
            Ls = list(subset)
            # Adding singletons to avoid strange cases like cycles or trees in candidates representation
            Ls += singletons
            # print("Ls: ", Ls)
            reorder_sets(Ls)
            if len(subset) >= m:
                m = len(subset)
                l_set = subset
        except ValueError:
            continue
    return m, l_set


################################################
# Functions used in development, to remove !!! #
################################################
def bygeneration():
    structure = generation(5, 20, 3)
    # print("preferences: ", structure['preferences'])
    size, largest_coherent_set = get_max_coherent_set(structure)
    print(size, largest_coherent_set)


def bygivenstruct1():
    str_example = {'nb_candidates': 5,
                   'preferences': [(1, [5, 3, 2, 4, Set([1])]),
                                   (1, [2, 4, Set([1, 3, 5])]), (1, [3, 5, 2, 4, Set([1])])],
                   'sum_vote_count': 3,
                   'candidates': {1: 'Candidate 1', 2: 'Candidate 2',
                                  3: 'Candidate 3', 4: 'Candidate 4', 5: 'Candidate 5'},
                   'nb_unique_orders': 3,
                   'nb_voters': 3}
    size, largest_coherent_set = get_max_coherent_set(str_example)
    print(size, largest_coherent_set)


def bygivenstruct2():
    str_example = {'nb_candidates': 4,
                   'preferences': [(1, [1, 2]), (1, [1, 3]), (1, [1, 4])],
                   'sum_vote_count': 3,
                   'candidates': {1: 'Candidate 1', 2: 'Candidate 2', 3: 'Candidate 3', 4: 'Candidate 4'},
                   'nb_unique_orders': 3,
                   'nb_voters': 3}

    size, largest_coherent_set = get_max_coherent_set(str_example)
    print(size, largest_coherent_set)


if __name__ == '__main__':
    bygeneration()
    # bygivenstruct1()
    # bygivenstruct2()


