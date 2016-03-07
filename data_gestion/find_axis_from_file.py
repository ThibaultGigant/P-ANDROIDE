from sage.all import Set
from file_gestion import *
from similarity_matrix import *
from time import time
from os import listdir
from os.path import join
from getopt import getopt
import sys


def find_axis_from_file(structure, dissimilarity_function=dissimilarity_over_over, weighted=False):
    """
    Finds the axes coherent with the data in the structure
    :param structure: data extracted from an election file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :return: calculation time and optimal permutations for this structure
    """
    candidates_set = Set(structure["candidates"].keys())

    t = time()
    similarity_matrix = create_similarity_matrix(structure, dissimilarity_function)
    optimal_permutations = find_permutation_dynamic_programming(similarity_matrix, candidates_set, {}, weighted)

    return time()-t, optimal_permutations[candidates_set]


def write_results_on_file(input_directory, output_file, dissimilarity_function=dissimilarity_over_over,
                          weighted=False, unwanted_candidates=[]):
    """
    For each file in the directory, calculates the optimal axes coherent with the data and writes it on the output file
    :param input_directory: directory where the .toc files are located
    :param output_file: output file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    """
    files = [join(input_directory, i) for i in listdir(input_directory) if i[-3:] == "toc"]
    fp = open(output_file, "w")

    for f in files:
        structure = read_file(f)
        if unwanted_candidates:
            structure = remove_unwanted_candidates(structure, unwanted_candidates)
        print(f)
        fp.write(str(f) + "\n")
        t, optimal_permutations = find_axis_from_file(structure, dissimilarity_function, weighted)
        print(t)
        fp.write("calculation time: " + str(t) + " seconds\n")
        fp.write("axes: " + str(optimal_permutations) + "\n")
        for axis in optimal_permutations[1]:
            fp.write(str([structure["candidates"][i] for i in axis]) + "\n")
        fp.write("\n")
    fp.close()


def write_directory_results_on_file(input_directory, output_file, dissimilarity_function=dissimilarity_over_over,
                                    weighted=False, unwanted_candidates=[]):
    """
    Creates a structure combining the data from all election files in the directory,
    then calculates the optimal axes coherent with the data and writes it on the output file
    :param input_directory: directory where the .toc files are located
    :param output_file: output file
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    """
    fp = open(output_file, "w")

    structure = read_directory(input_directory)
    if unwanted_candidates:
        structure = remove_unwanted_candidates(structure, unwanted_candidates)

    fp.write(str(input_directory) + "\n")
    t, optimal_permutations = find_axis_from_file(structure, dissimilarity_function, weighted)
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
    unwanted_candidates = []

    opts, args = getopt(sys.argv[1:], "d:o:w", ["func=", "fusion", "not="])

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

    if (not input_directory or not output_file) and len(args) != 2:
        raise IOError("Not enough arguments")

    if len(args) == 2:
        input_directory = args[0]
        output_file = args[1]

    if fusion:
        write_directory_results_on_file(input_directory, output_file, dissimilarity_function,
                                        weighted, unwanted_candidates)
    else:
        write_results_on_file(input_directory, output_file, dissimilarity_function, weighted, unwanted_candidates)


if __name__ == '__main__':
    launch()
