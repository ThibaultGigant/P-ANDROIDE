from sage.all import Set
from file_gestion import read_file
from similarity_matrix import *
from time import time
from os import listdir
from os.path import join
import sys


def find_axis_from_file(input_file, dissimilarity_function=dissimilarity_over_over, weighted=False):
    structure = read_file(input_file)
    candidates_set = Set(structure["candidates"].keys())

    t = time()
    similarity_matrix = create_similarity_matrix(structure, dissimilarity_function)
    optimal_permutations = find_permutation_dynamic_programming(similarity_matrix, candidates_set, {}, False)

    return time()-t, optimal_permutations[candidates_set]


def write_results_on_file(input_directory, output_file, dissimilarity_function=dissimilarity_over_over, weighted=False):
    files = [join(input_directory, i) for i in listdir(input_directory) if i[-3:] == "toc"]
    fp = open(output_file, "w")

    for f in files:
        print(f)
        fp.write(str(f) + "\n")
        t, optimal_permutations = find_axis_from_file(f, dissimilarity_function, weighted)
        print(t)
        fp.write("calculation time: " + str(t) + " seconds\n")
        fp.write("axes: " + str(optimal_permutations) + "\n\n")
    fp.close()


if __name__ == '__main__':
    write_results_on_file(sys.argv[1], sys.argv[2])
