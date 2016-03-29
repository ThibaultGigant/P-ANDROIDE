#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from generation import generation
from copy import copy
from time import time
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets, P, Q
from compiler.ast import flatten


def bandb(preferences, candidates, node=[], enum_list=[], best=0):
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

        if not node:
            tmp_set = []
        else:
            tmp_set, tmp_bound = copy(node)

        new_node = (tmp_set+[ballot], nb_voters)

        # Find compatible axes
        axes, nb_axes = find_axes2(new_node, candidates)

        #  Calculate the upper bound of new node
        if new_preferences:
            # Use axes to determine coherance and upper bound
            #new_bound = upper_bound(new_node, new_preferences, candidates)

            # Use comparision to determine coherence
            if axes:
                new_bound = upper_bound_bis(new_node[1], new_preferences, candidates, axes)
                new_node = (new_node[0], new_bound)

        enum_list += [new_node, (tmp_set, sum_nb_voters(new_preferences))]

        bandb(new_preferences, candidates, new_node, enum_list, best)
            # If only one axis was found, add the remaining ballots that are compatible with the axis
            #if nb_axes == 2:
            #    add_coherent_ballots(node, new_preferences, axes)

            #if nb_axes > 2:
                #v = sol(node, candidates, new_preferences, axes)
                #print ("V = " + str(v))
                #if v > best:
                #    best = v

                #print best, new_bound
            #    best += nb_voters

                # If node's upper_bound > best solution, branch
            #    if new_bound >= best:
            #        enum_list, best = bandb(new_preferences, candidates, new_node, enum_list, best)
    return enum_list, best

def bandb2(preferences, candidates, node=[], enum_list=[], best=([], 0)):
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

        if not node:
            tmp_set = []
        else:
            tmp_set, tmp_bound = copy(node)

        new_node = (tmp_set+[(nb_voters, ballot)], nb_voters)

        # Find compatible axes
        axes, nb_axes = find_axes2(new_node, candidates)

        # If axes exist
        if axes:
            if new_preferences:
                # Calculate node's upper bound
                #new_bound = upper_bound(new_node, new_preferences, candidates)
                new_bound = upper_bound_bis(new_node, new_preferences, candidates, axes)
                new_node = (new_node[0], new_bound)

                # If only one axis was found, add the remaining ballots that are compatible with the axis
                if nb_axes == 2:
                    new_node = add_coherent_ballots(new_node, new_preferences, axes)

                if nb_axes > 2:
                    # If more than two axes found, calculate optimal local solution
                    v = sol(new_node, candidates, new_preferences, axes)

                    # If local solution > current optimal solution, replace
                    if v[1] > best[1]:
                        best = v

                # If node's upper bound > best solution, branch
                if new_bound >= best[1]:
                    enum_list += [new_node, (tmp_set, sum_nb_voters(tmp_set, new_preferences))]
                    bandb2(new_preferences, candidates, new_node, enum_list, best)

    return enum_list, best

def transform_ballots(node):
    """
    Transforms ballots in node to Sets
    :param node: Current node ([ballot_set], upper_bound)
    :return: List of ballots as Set
    """
    L = []
    for nb_voters, ballot in node[0]:
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
    :param candidates: List of candidates
    :return: int
    """
    prefs, bound = node
    new_bound = 0
    for pref in prefs:
        new_bound += pref[0]

    for (nb_voters, ballot) in remaining_prefs:
        #print("Ballot to add : " + str(ballot))
        new_ballot_set = prefs + [(nb_voters, ballot)]
        #print("Ballot set : " + str(ballot_set) + " New ballot set : " + str(new_ballot_set))
        axes = find_axes2((new_ballot_set, bound), candidates)
        if axes:
            #print("Found axis : " + str(axes))
            new_bound = new_bound + nb_voters
    return new_bound

def upper_bound_bis(node, remaining_prefs, candidates, axes):
    """
    Calculates the node's upper bound
    :param node: Current node
    :param remaining_prefs: List of remaining ballots in preferences
    :param candidates: List of candidates
    :param axes: Compatible axes found at node
    :return: int
    """
    prefs, bound = node
    new_bound = 0
    for pref in prefs:
        new_bound += pref[0]

    for nb_voters, prefs in remaining_prefs:
        # Transform preference to set of ballot without indifference
        if isinstance(prefs[-1], int):
            ballot = Set(prefs)
        else:
            ballot = Set(prefs[:-1])
        # Determine whether the ballot is coherent with one of the axes
        for axis in axes:
            if is_coherent(ballot, axis):
                # If coherent, add ballot number of voters to the new bound
                new_bound += nb_voters
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
    candL = []
    ballots = transform_ballots(node)

    # Regrouper les bulletins qui contiennent le candidat c
    for c in candidates:
        S = Set([])
        for ballot in ballots:
            if c in ballot:
                S += Set([ballot])
        if S:
            S += Set([Set([c])])
        L += Set([S])
        candL += Set([S])
    # Transformer liste de Set en PQ-tree et aligner
    axes = P(L)
    for ballot in ballots:
        try:
            #print ("Align according to ballot : " + str(ballot))
            #print ("Axes :" + str(axes))
            axes.set_contiguous(ballot)
        except:
            return False, 0
    # Determiner les axes à partir des alignements trouvés
    all_axes = [] # Liste des axes
    for axis in axes.orderings():
        A = []
        for ballot_set in flatten(axis):
            if ballot_set:
                #A += [i+1 for i, x in enumerate(L) if x == ballot_set]
                A += [candL.index(ballot_set)+1]
        all_axes += [A]
    return all_axes, axes.cardinality()

def find_axes2(node, candidates):
    """
    Returns all possible coherent axes
    :param node: Current node ([ballot_set], upper_bound)
    :param candidates: List of candidates
    :return: List of possible axes, False if none found
    """
    L = []
    candL = []
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
            #print ("Align according to ballot : " + str(ballot))
            #print ("Axes :" + str(axes))
            axes.set_contiguous(ballot)
        except:
            return False, 0
    # Determiner les axes à partir des alignements trouvés
    all_axes = [] # Liste des axes
    for axis in axes.orderings():
        A = []
        for ballot_set in flatten(axis):
            #A += [i+1 for i, x in enumerate(L) if x == ballot_set]
            A += [L.index(ballot_set)+1]
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
            node = (node[0] + [(nb_voters, prefs)], node[1])
    return node

def sol(node, candidates, remaining_prefs, axes):
    """
    Calculates a local optimal solution
    :param v:
    :param node: Current node
    :param candidates: List of candidates
    :param remaining_prefs: List of remaining ballots in preferances
    :param axes: Compatible axes found at node
    :return: Value of local optimal solution
    """
    v = 0
    for (nb_voters, prefs) in node[0]:
        v += nb_voters

    for (nb_voters, prefs) in remaining_prefs:
        if isinstance(prefs[-1], int):
            ballot = Set(prefs)
        else:
            ballot = Set(prefs[:-1])
        axes, nb_axes = find_axes2(node, candidates)
        for axis in axes:
            if is_coherent(ballot, axis):
                v += nb_voters
                node = (node[0] + [(nb_voters, prefs)], node[1])
                break
    return (node, v)

def sum_nb_voters(prefs, remaining_prefs):
    """
    Calculcates upper_bound of an empty node
    :param remaining_prefs: List of remaining ballots in preferances
    :return: upper bound
    """
    bound = 0
    for pref in prefs:
        bound += pref[0]

    for node in remaining_prefs:
        bound += node[0]
    return bound

def nodes(n):
    t_nodes = 0
    for i in range(n):
        t_nodes += 2**(i+1)
    return t_nodes

def exemple():
    preferences = [(4, [3, 1, 2, Set([4, 5, 6, 7, 8, 9])]),
                   (3, [1, 7, 2, Set([3, 4, 5, 6, 8, 9])]),
                   (3, [5, 7, Set([1, 2, 3, 4, 6, 8, 9])]),
                   (2, [2, 7, 5, Set([1, 3, 4, 6, 8, 9])]),
                   (1, [8, 7, 1, Set([2, 3, 4, 5, 6, 9])]),
                   (1, [9, 2, 3, Set([1, 4, 5, 6, 7, 8])])]
    candidates = [i+1 for i in range(9)]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bandb2(preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")

def exemple_generation():
    structures, candidates = generation(8, 10)
    candidates = [i+1 for i in range(8)]
    preferences = structures["preferences"]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bandb2(preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")

if __name__ == '__main__':
    exemple()
    #exemple_generation()