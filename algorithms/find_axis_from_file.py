# -*- coding: utf-8 -*-
import sys
from os import getcwd
sys.path.append(getcwd())

from sage.all import Set
from data_gestion.file_gestion import *
from similarity_matrix import *
from time import time
from os import listdir
from os.path import join
from getopt import getopt
import sys


def find_axis_from_structure(structure, dissimilarity_function=dissimilarity_over_over,
                             weighted=False, unwanted_candidates=[]):
    """
    Finds the axes coherent with the data in the structure
    :param structure: data extracted from an election file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    :return: calculation time and optimal permutations for this structure
    """
    # candidates_set = Set(structure["candidates"].keys())

    # Creating a conversion table to make the calculations easier
    i = 1
    conversion_table = {}
    for candidate in structure["candidates"].keys():
        if candidate not in unwanted_candidates:
            conversion_table[i] = candidate
            i += 1

    t = time()
    similarity_matrix = create_similarity_matrix(structure, dissimilarity_function)

    candidates_set = Set(range(1, len(conversion_table)+1))
    candidates = [i-1 for i in conversion_table.values()]
    candidates.sort()

    optimal_permutations = find_permutation_dynamic_programming(similarity_matrix.matrix_from_rows_and_columns(candidates, candidates),
                                                                candidates_set, {}, weighted)

    res = (optimal_permutations[candidates_set][0], [[conversion_table[i] for i in l] for l in optimal_permutations[candidates_set][1]])

    return time()-t, res


def write_results_on_file(input_directory, output_file, dissimilarity_function=dissimilarity_over_over,
                          weighted=False, unwanted_candidates=[], strict=False):
    """
    For each file in the directory, calculates the optimal axes coherent with the data and writes it on the output file
    :param input_directory: directory where the .toc files are located
    :param output_file: output file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    :param strict: True if the file depicts strict preferences, False otherwise
    """
    files = [join(input_directory, i) for i in listdir(input_directory) if i[-3:] == "toc"]
    fp = open(output_file, "w")

    for f in files:
        structure = read_file(f, strict)
        print(f)
        fp.write(str(f) + "\n")
        t, optimal_permutations = find_axis_from_structure(structure, dissimilarity_function, weighted, unwanted_candidates)
        print(t)
        fp.write("calculation time: " + str(t) + " seconds\n")
        fp.write("axes: " + str(optimal_permutations) + "\n")
        for axis in optimal_permutations[1]:
            fp.write(str([structure["candidates"][i] for i in axis]) + "\n")
        fp.write("\n")
    fp.close()


def write_directory_results_on_file(input_directory, output_file, dissimilarity_function=dissimilarity_over_over,
                                    weighted=False, unwanted_candidates=[], strict=False):
    """
    Creates a structure combining the data from all election files in the directory,
    then calculates the optimal axes coherent with the data and writes it on the output file
    :param input_directory: directory where the .toc files are located
    :param output_file: output file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    :param strict: True if the file depicts strict preferences, False otherwise
    """
    fp = open(output_file, "w")

    structure = read_directory(input_directory, strict)

    fp.write(str(input_directory) + "\n")
    t, optimal_permutations = find_axis_from_structure(structure, dissimilarity_function, weighted, unwanted_candidates)
    print(t)
    fp.write("calculation time: " + str(t) + " seconds\n")
    fp.write("axes: " + str(optimal_permutations) + "\n")
    for axis in optimal_permutations[1]:
        fp.write(str([structure["candidates"][i] for i in axis]) + "\n")

    fp.close()


def launch():
    """
    Function used to launch the program the way we want it, using command line options
    :return:
    """
    dissimilarity_function = dissimilarity_over_over
    weighted = False
    input_directory = ""
    output_file = ""
    fusion = False
    strict = False
    unwanted_candidates = []

    opts, args = getopt(sys.argv[1:], "d:o:w", ["func=", "fusion", "not=", "strict"])

    for opt, value in opts:
        if opt == "-d":
            input_directory = value
        if opt == "-o":
            output_file = value
        if opt == "-w":
            weighted = True
        if opt == "--func":
            if value == "0":
                dissimilarity_function = dissimilarity_over_over
            elif value == "1":
                dissimilarity_function = dissimilarity_and_n
            elif value == "2":
                dissimilarity_function = dissimilarity_and_or
        if opt == "--fusion":
            fusion = True
        if opt == "--not":
            unwanted_candidates = list(map(int, value.split()))
        if opt == "--strict":
            strict = True

    if (not input_directory or not output_file) and len(args) != 2:
        raise IOError("Not enough arguments")

    if len(args) == 2:
        input_directory = args[0]
        output_file = args[1]

    if fusion:
        write_directory_results_on_file(input_directory, output_file, dissimilarity_function,
                                        weighted, unwanted_candidates, strict)
    else:
        write_results_on_file(input_directory, output_file, dissimilarity_function,
                              weighted, unwanted_candidates, strict)


if __name__ == '__main__':
    launch()
