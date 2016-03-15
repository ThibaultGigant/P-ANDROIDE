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
        (nb_voters, ballot) = new_preferences[0]
        new_preferences.remove((nb_voters, ballot))

        # Modification : start bound at nb_voters
        if not node:
            node = ([], 0)
            new_node = ([ballot], nb_voters)
        else:
            tmp_set, tmp_bound = copy(node)
            new_node = (tmp_set+[ballot], tmp_bound)

        # Modification : Start bound at 0
        #if not node:
        #    node = ([], 0)
        #tmp_set, tmp_bound = copy(node)
        #new_node = (tmp_set+[ballot], tmp_bound)

        # Find compatible axes and calculate the upper bound of node
        axes, nb_axes = find_axes(new_node, candidates)
        if new_preferences:
            # Modification : use axes to determine coherance and upper bound
            new_bound = upper_bound(new_node, new_preferences, candidates)

            # Modification
            #new_bound = upper_bound_bis(new_node[1], new_preferences, candidates, axes)
            new_node = (new_node[0],new_bound)

        enum_list += [new_node, copy(node)]

        # If no axis found
        #if axes == False:
        #    continue
        # If only one axis was found, add the remaining ballots that are compatible with the axis
        #if nb_axes == 2:
        #    add_coherent_ballots(node, new_preferences, axes)
        # Else, branch
        #else:
        #    bandb(new_preferences, new_node, enum_list)

        bandb(new_preferences, candidates, new_node, enum_list)
    return enum_list

def transform_ballots(node):
    """
    Transforms ballots in node to Sets
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

def upper_bound(node, remaining_prefs, candidates):
    """
    Calculates the node's upper bound
    :param node: Current node ([ballot_set], upper_bound)
    :param remaining_prefs: List of remaining ballots in preferances
    :return: int
    """
    #print("Upper Bound :" + str(node))
    #print("Remaining prefs :" + str(remaining_prefs))
    (ballot_set, bound) = node
    new_bound = bound
    for (nb_voters, ballot) in remaining_prefs:
        #print("Ballot to add : " + str(ballot))
        new_ballot_set = ballot_set + [ballot]
        #print("Ballot set : " + str(ballot_set) + " New ballot set : " + str(new_ballot_set))
        axes = find_axes((new_ballot_set, bound), candidates)
        if axes:
            #print("Found axis : " + str(axes))
            new_bound = new_bound + nb_voters
    return new_bound

# Modification : upper_bound without calling find_axe function
def upper_bound_bis(bound, remaining_prefs, candidates, axes):
    """
    Calculates the node's upper bound
    :param bound: Current node's upper bound
    :param remaining_prefs: List of remaining ballots in preferences
    :return: int
    """
    new_bound = bound
    for (nb_voters, prefs) in remaining_prefs:
        # Transform preference to set of ballot without indifference
        if isinstance(prefs[-1], int):
            ballot = Set(prefs)
        else:
            ballot = Set(prefs[:-1])

        # Determine whether the ballot is coherent with one of the axes
        for axis in axes:
            if is_coherent(ballot, axis):
                # If coherent, add ballot number of voters to the new bound
                new_bound = new_bound + nb_voters
                break
    return new_bound

def find_axes(node, candidates):
    """
    Returns all possible coherent axes
    :param node: Current node ([ballot_set], upper_bound)
    :param candidates: List of candidates
    :return: List of possible axes, False if none found
    """
    L = []
    ballots = transform_ballots(node)

    # Regrouper les bulletins qui contiennent le candidat c
    for c in candidates:
        S = Set([])
        for ballot in ballots:
            if c in ballot:
                S += Set([ballot])
        S += Set([Set([c])])
        L += Set([S])

    # Transformer liste de Set en PQ-tree et aligner
    axes = P(L)
    for ballot in ballots:
        try:
            axes.set_contiguous(ballot)
        except:
            return False, 0

    # Determiner les axes à partir des alignements trouvés
    all_axes = [] # Liste des axes
    for axis in axes.orderings():
        # TODO remove all parentheses
        A = []
        for pq in axis:
            for ballot_set in pq:
                if isinstance(ballot_set[0],int) or not ballot_set:
                    A += [i+1 for i, x in enumerate(L) if x == Set([ballot_set])]
                else:
                    A += [i+1 for i, x in enumerate(L) if x == ballot_set]
        all_axes += [A]
    return all_axes, axes.cardinality()

def is_coherent(ballot, axes):
    """
    Determines if a ballot is coherent with a given axis
    :param ballot: a ballot for candidates
    :param axis: axis of preference
    :return: True if the ballot is coherent with the axis
    """
    return any(ballot == Set(axes[i:i + len(ballot)]) for i in range(len(axes) - len(ballot) + 1))

def add_coherent_ballots(node, remaining_prefs, axes):
    """
    Adds the remaining ballots that are coherent with the axis to node
    :param node: Current node ([ballot_set], upper_bound)
    :param remaining_prefs: List of remaining ballots in preferances
    :param axes: List of axes (in this case, only one axis)
    :return: List of ballots
    """
    for (nb_voters, prefs) in remaining_prefs:
        if isinstance(prefs[-1], int):
            ballot = Set(prefs)
        else:
            ballot = Set(prefs[:-1])
    if is_coherent(ballot, axes[0]):
        if axes:
            node[0] = node[0] + [prefs]

def exemple1():
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
    axes, card = find_axes(node, c)
    print axes, card

def exemple2():
    node = ([[4, 7, 2, 8, 10, {1, 3, 5, 6, 9}],
              [10, 8, 7, 4, 2, {1, 3, 5, 6, 9}],
              [5, 1, 6, 2, 4, {8, 9, 10, 3, 7}],
              [6, 9, 1, 5, 2, {8, 10, 3, 4, 7}],
              [9, 6, 1, 5, 2, {8, 10, 3, 4, 7}]],20)
    c = [i for i in range(1,11)]
    axes, card = find_axes(node, c)
    print axes, card

def exemple3():
    node = ([[1, 2],
             [2, 3],
             [3, 4],
             [2, 5]],20)
    c = [i for i in range(1,6)]
    axes, card = find_axes(node, c)
    print axes, card

def exemple4():
    node = ([[3,4,1,Set([2])],
             [2,1,3,Set([4])]],20)
    c = [i for i in range(1,5)]
    axes, card = find_axes(node, c)
    print axes

if __name__ == '__main__':
    #structure, candidates = generation(4, 3, 3)
    #preferences = structure["preferences"]
    preferences = [(1, [3, 4, 1, Set([2])]), (1, [2, 1, 3, Set([4])]), (1, [1, 3, 4, Set([2])])]
    candidates = [i for i in range(1,5)]
    print("Preferences : " + str(preferences))
    bb = bandb(preferences, candidates, [], [])
    print("Branch and Bound :")
    print bb