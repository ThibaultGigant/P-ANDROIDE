#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from generation import generation
from copy import copy
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets, P, Q


def bandb(preferences, candidates, node, enum_list):
    """
    Branch and Bound
    :param preferences: List of ballots : (number of voters, ballot)
    :param candidates: List of candidates
    :param node: current node
    :param enum_list:
    :return: List of leaves enum_list
    """
    new_preferences = copy(preferences)
    while new_preferences:
        (nb_voters,ballot) = new_preferences[0]
        new_preferences.remove((nb_voters,ballot))
        if node == []:
            node = ([],0)
        tmp_set, tmp_bound = copy(node)
        new_node = (tmp_set+[ballot],tmp_bound)

        # Caluclate upper node
        #new_bound = upper_bound(new_node,preferences_bis)
        #new_node = (new_node[0],new_bound)

        enum_list += [new_node, copy(node)]

        # Find compatible axes
        #nb_axes, axes = find_axes(new_node)

        # If no axis found
        #if axes == False:
        #    continue
        # If only one axis was found, add the remaining ballots that are compatible with the axis
        #if nb_axes == 1:
        #    add_coherent_ballots(node, new_preferences)
        # Else, branch
        #else:
        #    bandb(new_preferences, new_node, enum_list)

        bandb(new_preferences, candidates, new_node, enum_list)
    return enum_list

def find_axes(node, candidates):
    """
    Returns all possible coherent axes
    :param node: Current node ([ballot_set], upper_bound)
    :param candidates: List of candidates
    :return: List of possible axes, False if none found
    """
    L = []
    ballots = transform_ballots(node)
    for c in candidates:
        S = Set([])
        for ballot in ballots:
            if c in ballot:
                S += Set([ballot])
        if not S.is_empty():
            L += Set([S])
    # print L

    ##### Find number of axes
    # A = reorder_sets(L)
    # return A, A.cardinality()

    return reorder_sets(L)

def transform_ballots(node):
    """
    Transforms ballot in node to a Set
    :param node: Current node ([ballot_set], upper_bound)
    :return: List of ballots as Set
    """
    L = []
    for ballot in node[0]:
        if isinstance(ballot[-1], int):
            L.append(Set(ballot))
        else:
            L.append(Set(ballot[:-1]))
    return L

def add_coherent_ballots(node, remaining_prefs):
    """
    Adds the remaining ballots that are coherent with the axis to node
    :param node: Current node ([ballot_set], upper_bound)
    :param remaining_prefs: List of remaining ballots in preferances
    :return: List of ballots
    """
    for (nb_voters, ballot) in remaining_prefs:
        axes = find_axes(node[0]+[ballot])
        if axes:
            node[0] = node[0] + [ballot]

def upper_bound(node, remaining_prefs):
    """
    Calculates the node's upper bound
    :param node: Current node ([ballot_set], upper_bound)
    :param remaining_prefs: List of remaining ballots in preferances
    :return: int
    """
    (ballot_set, bound) = node
    for (nb_voters, ballot) in remaining_prefs:
        new_ballot_set = ballot_set + [ballot]
        if find_axes(new_ballot_set):
            new_bound = bound + nb_voters
    return new_bound

if __name__ == '__main__':
    #structure, candidates = generation(5, 3, 3)
    #preferences = structure["preferences"]
    #print(bandb(preferences, candidates, [], []))

    node = ([[6, 5, 9, {1, 2, 3, 4, 7, 8, 10}],
             [4, 7, 3, {1, 2, 5, 6, 8, 9, 10}],
             [2, 1, 10, {3, 4, 5, 6, 7, 8, 9}],
             [9, 6, 5, {1, 2, 3, 4, 7, 8, 10}],
             [2, 7, 4, {1, 3, 5, 6, 8, 9, 10}],
             [7, 2, 1, {3, 4, 5, 6, 8, 9, 10}],
             [2, 7, 1, {3, 4, 5, 6, 8, 9, 10}],
             [2, 1, 7, {3, 4, 5, 6, 8, 9, 10}],
             [5, 6, 9, {1, 2, 3, 4, 7, 8, 10}]],20)
    c = [i for i in range(1,11)]
    print find_axes(node,c)