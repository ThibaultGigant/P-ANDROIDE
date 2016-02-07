#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from sage.all import Set, matrix
from itertools import permutations, combinations
from generation import generation


def create_similarity_matrix(structure):
    """
    Creates the similarity matrix between candidates, given the preferences stored in the structure
    :param structure: data extracted from an election file
    :return: similarity matrix
    :rtype: matrix
    """
    # Variables initialization
    nb_candidates = structure["nb_candidates"]
    similarity_m = [[0 for _ in range(nb_candidates)] for _ in range(nb_candidates)]
    preferences = structure["preferences"]
    vote_count = float(structure["sum_vote_count"])

    for ballot in preferences:
        # Removing set of indifference if any
        if isinstance(ballot[1][-1], int):
            temp = ballot[1]
        else:
            temp = ballot[1][:-1]
        # Updating the similarity matrix for each pair of candidates in the ballot
        if len(temp) >= 2:
            # recuperation of pairs of candidates in the ballot
            pairs = combinations(temp, 2)
            for candidate1, candidate2 in pairs:
                similarity_m[candidate1-1][candidate2-1] += 1 * ballot[0]
                similarity_m[candidate2-1][candidate1-1] += 1 * ballot[0]

    for line in range(nb_candidates):
        for element in range(nb_candidates):
            similarity_m[line][element] = 1 - similarity_m[line][element]/vote_count

    return matrix(similarity_m)


def get_matrix_score(mat):
    """
    Calculates matrix gradient score
    :param mat: similarity matrix between candidates
    :type mat: matrix
    :return: matrix gradient score
    :rtype: int
    """
    rows = mat.nrows()
    cols = mat.ncols()
    score_m = 0

    # Calculates score
    for i in range(rows):
        for j in range(i+1, cols-1):
            for k in range(j+1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    score_m += 1
                # per column
                if mat[-i-1][-j-1] > mat[-i-1][-k-1]:
                    score_m += 1

    return score_m


def get_weighted_matrix_score(mat):
    """
    Calculates the matrix's weighted gradient score
    :param mat: similarity matrix between candidates
    :type mat: matrix
    :return: weighted gradient score
    :rtype: int
    """
    rows = mat.nrows()
    cols = mat.ncols()
    wscore_m = 0

    # Calculates score
    for i in range(rows):
        for j in range(i+1, cols-1):
            for k in range(j+1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    wscore_m += mat[i][j] - mat[i][k]
                # per column
                if mat[-i-1][-j-1] > mat[-i-1][-k-1]:
                    wscore_m += mat[-i-1][-j-1] - mat[-i-1][-k-1]

    return wscore_m


def find_permutation_naive(structure, weighted=False):
    """
    Calculate the similarity matrix between candidates then finds the permutation maximizing the matrix gradient score
    :param structure: data extracted from an election file
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :type weighted: bool
    :return: list of candidates indices = axis of candidates
    :rtype: list
    """
    # Variables initialization
    candidates_id = range(structure["nb_candidates"])
    candidates_permutations = list(permutations(candidates_id, structure["nb_candidates"]))
    similarity_matrix = create_similarity_matrix(structure)

    # Calculating scores for all possible permutations
    if weighted:
        scores = [get_weighted_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(i), list(i))) for i in candidates_permutations]
    else:
        scores = [get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(i), list(i))) for i in candidates_permutations]

    # Recuperation of the best permutation's index, then returning the corresponding permutation
    max_score_index = scores.index(min(scores))
    return candidates_permutations[max_score_index]


################################################
# Functions used in development, to remove !!! #
################################################
def example1():
    structure = {'nb_candidates': 5,
                 'preferences': [(1, [5, 3, 2, 4, Set([1])]), (4, [2, 4, Set([1, 3, 5])]), (1, [3, 5, 4, Set([1])])],
                 'sum_vote_count': 6,
                 'candidates': {1: 'Candidate 1', 2: 'Candidate 2', 3: 'Candidate 3', 4: 'Candidate 4', 5: 'Candidate 5'},
                 'nb_unique_orders': 3,
                 'nb_voters': 6}
    mat = create_similarity_matrix(structure)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    optimal_permutation = find_permutation_naive(structure)
    print("Optimal permutation: ", optimal_permutation)
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example2():
    structure = generation(7, 20)
    mat = create_similarity_matrix(structure)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    optimal_permutation = find_permutation_naive(structure)
    print("Optimal permutation: ", [i+1 for i in optimal_permutation])
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


if __name__ == '__main__':
    # example1()
    example2()
