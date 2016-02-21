#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
from random import shuffle, randint, choice
from sage.all import Set


def bfs(cand_list, favorite):
    """
    Creates a list from the element with the given index
    :param cand_list: sorted list of candidates (their ID)
    :param favorite: index of the favorite candidate, to place first in the list
    :return: list simulating a BFS from the element with the given index
    """
    left_right = [list(reversed(cand_list[:favorite])), cand_list[favorite+1:]]
    pref = [cand_list[favorite]]
    # if there's an empty list, you can't choose from it...
    if [] in left_right:
        left_right.remove([])
    # picking a candidate to add to the list on one side (left or right) of the already chosen candidates
    while left_right:
        pick = choice(left_right)
        pref.append(pick.pop(0))
        if not pick:
            left_right.remove(pick)

    return pref


def generation(nb_candidates, nb_ballots, nb_prefs=None):
    """
    Randomly generates fictional ballots
    :param nb_candidates: number of candidates
    :param nb_ballots: number of ballots to generate
    :param nb_prefs: if specified, number of strict preferences for each ballot
    :return: same structure returned by the lecture of a file
    """

    # Creation of the map of candidates
    candidates = {i: "Candidate " + str(i) for i in range(1, nb_candidates+1)}
    # Creation of a list of candidates, shuffled to simulate some sort of classification
    cand_list = list(range(1, nb_candidates+1))
    shuffle(cand_list)
    print("The randomly generated candidates order is: ", cand_list)

    # Creation of ballots
    ballots = []
    rand_prefs = nb_prefs is None
    for _ in range(nb_ballots):
        favorite = randint(0, nb_candidates-1)  # index of favorite candidate for this ballot
        pref = bfs(cand_list, favorite)
        if rand_prefs:
            nb_prefs = randint(1, nb_candidates)  # number of strict preferences for this ballot
        temp = pref[:nb_prefs]
        temp.append(Set(pref[nb_prefs:]))
        ballots.append(temp)

    # Creation of the list of preferences
    prefs = []
    while ballots:
        ballot = ballots.pop()
        prefs.append((ballots.count(ballot)+1, ballot))
        while ballot in ballots:
            ballots.remove(ballot)

    # Sort preferences by number of voters
    prefs.sort(key=lambda x: x[0], reverse=True)

    return {"nb_candidates": nb_candidates,
            "candidates": candidates,
            "nb_voters": nb_ballots,
            "sum_vote_count": nb_ballots,
            "nb_unique_orders": len(prefs),
            "preferences": prefs}, cand_list


if __name__ == '__main__':
    structure, c_list = generation(10, 10, 3)
    for i in structure["preferences"]:
        print(i)
