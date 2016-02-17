#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
from generation import generation
from sage.all import Set
from sage.graphs.pq_trees import reorder_sets
from itertools import chain, combinations
from random import shuffle


def is_coherent(ballot, axis):
    """
    Determines if a ballot is coherent with a given axis
    :param ballot: a ballot for candidates
    :param axis: axis of preference
    :return: True if the ballot is coherent with the axis
    """
    return any(ballot == Set(axis[i:i + len(ballot)]) for i in range(len(axis) - len(ballot) + 1))


def is_set_coherent(ballot_list, axis):
    """
    Determines if the set of ballots is coherent with a given axis
    :param ballot_list: set of ballots for candidates
    :param axis: axis of preference
    :return: True if all the ballots in the set are coherent with the axis
    """
    return all(is_coherent(ballot, axis) for ballot in ballot_list)


def ballot_generation():
    structure, axis = generation(5, 10, 3)
    L = []
    for ballot in structure["preferences"]:
        if isinstance(ballot[1][-1], int):
            L.append(Set(ballot[1]))
        else:
            L.append(Set(ballot[1][:-1]))
    return L, axis


if __name__ == '__main__':
    # A=[1,5,2,6,3,4]
    # B=[Set([5,3,6,2]),Set([1,2,5])]
    # Bs=Set([Set([5,3,6,2]),Set([1,2,5])])
    # print(is_set_coherent(B,A))
    ballot_s, axis = ballot_generation()
    print("Axis before shuffle: " + str(axis))
    if is_set_coherent(ballot_s, axis):
        print("The generated set of ballots is coherent with this axis")
    else:
        print("The generated set of ballots isn't coherent with this axis")
    shuffle(axis)
    print("Axis after shuffle: " + str(axis))
    if is_set_coherent(ballot_s, axis):
        print("The generated set of ballots is coherent with this axis")
    else:
        print("The generated set of ballots isn't coherent with this axis")
