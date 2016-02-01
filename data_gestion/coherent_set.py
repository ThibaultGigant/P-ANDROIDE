#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-
import sys
from data_gestion.file_gestion import read_file


def get_max_coherent_set(structure):
    """
    Finds the largest coherent set of ballots
    :param structure: data extracted from an election file
    :return: largest coherent set of ballots
    """
    pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("This program takes one and only one argument")
    filename = sys.argv[1]
    structure = read_file(filename)
    print(structure["candidates"])
    print(structure["preferences"])
