#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-


import sys
from os import getcwd
sys.path.append(getcwd())

from data_gestion.generation import generation
from data_gestion.file_gestion import read_file
from copy import copy
from time import time
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets, P, Q
from compiler.ast import flatten

def bnb(nvar, preferences, candidates, node=([], 0), enum_list=[], best=([], 0), i=0):
    #print("Debut bnb :")
    #print ("Preferences : " + str(preferences))
    #print ("Enum List : " + str(enum_list))
    if preferences:
        #for nb_voters, ballot in preferences:

        nb_voters, ballot = preferences[0]
        new_preferences = copy(preferences)
        new_preferences.remove((nb_voters, ballot))

        copyNodeSet, copyNodeBound = copy(node)

        nodeSetL = copyNodeSet+[(nb_voters, ballot)]
        nodeSetR = copyNodeSet
        i+=1

        axesL, nb_axesL = find_axes(nodeSetL, candidates)
        if axesL:
            nodeBoundL = upper_bound(nodeSetL, new_preferences, candidates, axesL)
            nodeL = (nodeSetL, nodeBoundL)

            if nb_axesL == 2:
                nodeL = add_coherent_ballots(nodeL, new_preferences, axesL)

            if nb_axesL > 2 and i==nvar:
                # If more than two axes found, calculate optimal local solution
                v = sol(nodeL, candidates, new_preferences)

                # If local solution > current optimal solution, replace
                if v[1] > best[1]:
                    best = v

            if nodeBoundL > best[1]:
                enum_list += [nodeL]
                enum_list, best = bnb(nvar, new_preferences, candidates, nodeL, enum_list, best, i)

        #axesR, nb_axesR = find_axes2(nodeSetR, candidates)
        if not nodeSetR:
            nodeBoundR = sum_nb_voters(nodeSetR, new_preferences)
        else:
            nodeBoundR = copyNodeBound
        nodeR = (nodeSetR, nodeBoundR)

        #if axesPrev == 2:
        #    nodeR = add_coherent_ballots(nodeR, new_preferences, axes)

        if i==nvar:
            #If more than two axes found, calculate optimal local solution
            v = sol(nodeR, candidates, new_preferences)

            # If local solution > current optimal solution, replace
            if v[1] > best[1]:
                best = v

        if nodeBoundR > best[1]:
            enum_list += [nodeR]
            enum_list, best = bnb(nvar, new_preferences, candidates, nodeR, enum_list, best, i)

    return enum_list, best


def transform_ballots(nodeSet):
    """
    Transforms ballots in node to Sets
    :param nodeSet: Current node ([ballot_set], upper_bound)
    :return: List of ballots as Set
    """
    L = []
    for nb_voters, ballot in nodeSet:
        if isinstance(ballot[-1], int):
            L.append(Set(ballot))
        else:
            L.append(Set(ballot[:-1]))
    return L

#def bounds(node, remaining_prefs, candidates, axes):


def upper_bound(nodeSet, remaining_prefs, candidates, axes):
    """
    Calculates the node's upper bound
    :param nodeSet: Current node set of prefs
    :param remaining_prefs: List of remaining ballots in preferences
    :param candidates: List of candidates
    :param axes: Compatible axes found at node
    :return: int
    """
    new_bound = 0
    for pref in nodeSet:
        new_bound += pref[0]

    for nb_voters, pref in remaining_prefs:
        # Transform preference to set of ballot without indifference
        if isinstance(pref[-1], int):
            ballot = Set(pref)
        else:
            ballot = Set(pref[:-1])
        # Determine whether the ballot is coherent with one of the axes
        for axis in axes:
            if is_coherent(ballot, axis):
                # If coherent, add ballot number of voters to the new bound
                new_bound += nb_voters
                break
    return new_bound

def sol(node, candidates, remaining_prefs):
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
        axes, nb_axes = find_axes2(node[0], candidates)
        for axis in axes:
            if is_coherent(ballot, axis):
                v += nb_voters
                node = (node[0] + [(nb_voters, prefs)], node[1])
                break
    return (node, v)

def find_axes(nodeSet, candidates):
    """
    Returns all possible coherent axes
    :param nodeSet: Current node ([ballot_set], upper_bound)
    :param candidates: List of candidates
    :return: List of possible axes, False if none found
    """
    L = []
    candL = []
    ballots = transform_ballots(nodeSet)

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

def find_axes2(nodeSet, candidates):
    """
    Returns all possible coherent axes
    :param node: Current node ([ballot_set], upper_bound)
    :param candidates: List of candidates
    :return: List of possible axes, False if none found
    """
    L = []
    candL = []
    ballots = transform_ballots(nodeSet)
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

def is_coherent2(ballot, axes):
    """
    Determines if a ballot is coherent with a given axis
    :param ballot: a ballot for candidates
    :param axis: axis of preference
    :return: True if the ballot is coherent with the axis
    """
    sub = Set([])
    for candidate in ballot:
        if candidate in axes:
            sub += Set([candidate])
    if sub:
        if len(sub) == len(ballot):
            coherent = any(ballot == Set(axes[i:i + len(ballot)]) for i in range(len(axes) - len(ballot) + 1))
        else:
            coherent = (sub == Set(axes[0:len(sub)]) or sub == Set(axes[len(axes)-len(sub):]))
    else:
        coherent = True
    return coherent

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
    bb, best = bnb(preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")

def exemple2():
    preferences = [(4, [3, 9, 2, Set([1, 4, 5, 6, 7, 8])]),
                   (4, [1, 8, Set([2, 3, 4, 5, 6, 7, 9])]),
                   (3, [3, 5, 7, Set([1, 2, 4, 6, 8, 9])]),
                   (2, [7, 5, Set([1, 2, 3, 4, 6, 8, 9])]),
                   (2, [9, 7, 2, Set([1, 3, 4, 5, 6, 8])]),
                   (2, [9, 7, 6, Set([1, 2, 3, 4, 5, 8])]),
                   (1, [9, 4, 6, Set([1, 2, 3, 5, 7, 8])]),
                   (1, [1, 7, 8, Set([2, 3, 4, 5, 6, 9])]),
                   (1, [9, 2, Set([1, 3, 4, 5, 6, 7, 8])])]
    candidates = [i+1 for i in range(9)]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bnb(len(preferences), preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")

def exemple3():
    preferences = [(10, [2, 7, 8, Set([1, 3, 4, 5, 6])]),
                   (10, [2, 5, 6, Set([1, 3, 4, 7, 8])]),
                   (1, [1, 2, 3, Set([4, 5, 6, 7, 8])])]
    candidates = [i+1 for i in range(8)]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bnb(len(preferences),preferences, candidates)
    t2 = time()
    f = "_resultat.txt"
    wfile = open(f, 'w')
    wfile.write("Plus large ensemble cohérent : " + str(best[0][0]) + "\n")
    wfile.write("Resultat : " + str(best[1]) + "\n")
    wfile.write("Duration : " + str(t2-t1) + "\n")
    wfile.write("Axes :\n")
    axes, card = find_axes2(best[0][0], candidates)
    for a in axes:
        wfile.write(str(a)+"\n")
    wfile.close()

def exemple4():
    preferences = [(10, [1, 2, 3, Set([4, 5, 6, 7, 8, 9, 10, 11])]),
                   (10, [5, 6, 7, Set([1, 2, 3, 4, 8, 9, 10, 11])]),
                   (1, [9, 10, 11, Set([1, 2, 3, 4, 5, 6, 7, 8])])]
    candidates = [i+1 for i in range(8)]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bnb(len(preferences),preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")
    for enum in bb:
        print enum

def exemple_generation():
    structures, candidates = generation(8, 10)
    candidates = [i+1 for i in range(8)]
    preferences = structures["preferences"]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bnb(len(preferences), preferences, candidates)
    t2 = time()
    print ("Best solution : " + str(best))
    #print bb
    print("Duration : " + str(t2-t1))
    print("On explore " + str(len(bb)) + " noeuds parmi " + str(nodes(len(preferences))) + " noeuds.")

def exemple_file():
    structure = read_file(sys.argv[1])
    preferences = structure["preferences"]
    candidates = [i+1 for i in range(len(structure["candidates"]))]
    print("Preferences : " + str(preferences))
    print("Candidats : " + str(candidates))
    t1 = time()
    bb, best = bnb(len(preferences), preferences, candidates)
    t2 = time()
    print("done")
    f = sys.argv[1].split(".")[0]  + "_resultat.txt"
    wfile = open(f, 'w')
    wfile.write("Plus large ensemble cohérent : " + str(best[0][0]) + "\n")
    wfile.write("Resultat : " + str(best[1]) + "\n")
    wfile.write("Duration : " + str(t2-t1) + "\n")
    wfile.write("Axes :\n")
    axes, card = find_axes2(best[0][0], candidates)
    if axes:
        for a in axes:
            wfile.write(str(a)+"\n")
    wfile.close()

if __name__ == '__main__':
    #exemple()
    #exemple2()
    #exemple_generation()
    #exemple3()
    exemple_file()
