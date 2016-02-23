#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

import sys
from file_gestion import read_file
from generation import generation


class Tree:
    """
    Binary tree
    The left and right attributes are trees or None if the Tree actually is a leaf
    """
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.subset = data

    def __str__(self):
        return str(self.subset) + "\nLeft: " + self.left.__str__() + "\nRight: " + self.right.__str__() + "\n"

    def leaves_number(self):
        """
        Counts the number of leaves of the tree
        :return: number of leaves
        :rtype: int
        """
        if self.is_leaf():
            return 1
        else:
            return self.left.leaves_number() + self.right.leaves_number()

    def nodes_number(self):
        """
        Returns the number of nodes in the tree
        :rtype: int
        """
        if self.is_leaf():
            return 1
        else:
            return 1 + self.left.nodes_number() + self.right.nodes_number()

    def is_leaf(self):
        """
        Returns True if the instance is a leaf
        :rtype: bool
        """
        return self.left is None and self.right is None


def build_enumeration_tree(ballots_list, index=0):
    """
    Builds a tree enumerating all possible subsets of ballots from the given list of ballots.
    It will order the tree according to the ballots list. It is recommended to give a sorted list of ballots.
    :param ballots_list: list of ballots
    :param index: index of the ballot we're dealing with at this iteration
    :type ballots_list: list
    :type index: int
    :return: the enumeration tree
    """
    if index < len(ballots_list) - 1:
        left = ballots_list[:]
        right = ballots_list[:]
        right.pop(index)
        return Tree(ballots_list,
                    build_enumeration_tree(left, index+1),
                    build_enumeration_tree(right, index))
    elif index == len(ballots_list) - 1:
        left = ballots_list[:]
        right = ballots_list[:]
        right.pop(index)
        return Tree(ballots_list,
                    Tree(left, None, None),
                    Tree(right, None, None))


################################################
# Functions used in development, to remove !!! #
################################################
def example1():
    if len(sys.argv) != 2:
        sys.exit("This program takes one and only one argument")
    file = sys.argv[1]
    structure = read_file(file)
    ballots = [ballot[1] for ballot in structure["preferences"]]
    print(ballots)
    print(build_enumeration_tree(ballots))


def example2():
    structure = generation(5, 7)
    ballots = [ballot[1] for ballot in structure["preferences"]]
    print(ballots)
    # print(build_enumeration_tree(ballots))
    enumeration_tree = build_enumeration_tree(ballots)
    print("Number of unique votes: " + str(structure["nb_unique_orders"]) +
          ", so there should be " + str(2**structure["nb_unique_orders"]) + " leaves")
    print("Number of leaves: " + str(enumeration_tree.leaves_number()))
    print("Number of nodes: " + str(enumeration_tree.nodes_number()))


if __name__ == '__main__':
    # example1()
    example2()
