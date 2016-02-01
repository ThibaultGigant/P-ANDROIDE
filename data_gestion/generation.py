#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
from random import shuffle, randint, choice
from sage.all import Set


def bfs(cand_list, favorite):
    """
    Creates a list simulating a BFS from the element with the given index
    :param cand_list: sorted list of candidates (their ID)
    :param favorite: index of the favorite, to place first in the list
    :return: list simulating a BFS from the element with the given index
    """
    left_right = [-1, 1]
    pref = [cand_list[favorite]]
    for i in range(1, min(favorite+1, len(cand_list) - favorite + 1)):
        c = choice(left_right)
        if len(cand_list) > favorite + i * c >= 0:
            pref.append(cand_list[favorite + i * c])
        if len(cand_list) > favorite + i * -c >= 0:
            pref.append(cand_list[favorite + i * -c])
    return pref


def generation(nb_candidates, nb_ballots, nb_prefs = None):
    """
    Randomly generates fictional ballots
    :param nb_candidates: number of candidates
    :param nb_ballots: number of ballots to generate
    :param nb_prefs: if specified, number of strict preferences for each ballot
    :return: same structure returned by the lecture of a file
    """

    # Creation of the map of candidates
    candidates = {i: "Candidate " + str(i) for i in range(nb_candidates+1)}
    # Creation of a list of candidates, shuffled to simulate some sort of classification
    cand_list = shuffle(list(range(1, nb_candidates+1)))

    # Creation of ballots
    ballots = []
    rand_prefs = nb_prefs is None
    for _ in range(nb_ballots):
        favorite = randint(0, nb_candidates-1)  # favorite candidate for this ballot
        pref = bfs(cand_list, favorite)
        if rand_prefs:
            nb_prefs = randint(nb_candidates)  # number of strict preferences for this ballot
        ballots.append(pref[:nb_prefs] + Set(pref[nb_prefs:]))

    ballots_set = Set(ballots)
    prefs = []
    for ballot in ballots_set:
        prefs.append((ballots.count(ballot), ballot))

    return {"nb_candidates": nb_candidates,
            "candidates": candidates,
            "nb_voters": nb_ballots,
            "sum_vote_count": nb_ballots,
            "nb_unique_orders": len(prefs),
            "preferences": prefs}
