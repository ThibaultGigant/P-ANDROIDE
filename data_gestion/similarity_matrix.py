#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from sage.all import Set, matrix
from itertools import permutations


def create_similarity_matrix(structure):
    """
    Creates the similarity matrix between candidates, given the preferences stored in the structure
    :param structure: data extracted from an election file
    :return: similarity matrix
    :rtype: matrix
    """
    nb_candidates = structure["nb_candidates"]
    similarity_m = [[] for _ in range(nb_candidates)]
    preferences = structure["preferences"]

    for i in range(nb_candidates):
        for j in range(nb_candidates):
            similarity = 0
            if i == j:
                similarity_m[i] += [0]
            else:
                for ballot in preferences:
                    # For each pair of candidates (i,j), find number of ballots containing them both
                    if (i+1 in ballot[1]) and (j+1 in ballot[1]):
                        similarity += ballot[0]
                similarity_m[i] += [1-float(similarity)/structure["sum_vote_count"]]
    return matrix(similarity_m)


def get_matrix_score(mat):
    """
    Calculates matrix gradient score
    :param mat: similarity matrix between candidates
    :type mat: matrix
    :return: matrix gradient score
    :rtype: matrix
    """
    rows = mat.nrows()
    cols = mat.ncols()
    score_m = [[] for i in range(rows)]
    # Calculates score per row
    for i in range(rows):
        for j in range(i, cols):
            t_score = 0
            for k in range(j, cols):
                if mat[i][j] > mat[i][k]:
                    t_score += 1
            score_m[i] += [t_score]
            if i != j:
                score_m[j] += [t_score]
    # Adds the score calculated per column
    for j in reversed(range(cols)):
        for i in reversed(range(j)):
            t_score = 0
            for k in range(i):
                if (mat[i][j] > mat[k][j]):
                    t_score += 1
            score_m[i][j] += t_score
            score_m[j][i] += t_score
    return matrix(score_m)


def get_weighted_matrix_score(mat):
    """
    Calculates the matrix's weighted gradient score
    :param mat: similarity matrix between candidates
    :type mat: matrix
    :return: weighted gradient score
    :rtype: matrix
    """
    rows = mat.nrows()
    cols = mat.ncols()
    wscore_m = [[] for i in range(rows)]
    # Calculates score per row
    for i in range(rows):
        for j in range(i,cols):
            t_score = 0
            for k in range(j,cols):
                if (mat[i][j]>mat[i][k]):
                    t_score += mat[i][j]-mat[i][k]
            wscore_m[i] += [t_score]
            if (i != j):
                wscore_m[j] += [t_score]
    # Calculates score per column
    for j in reversed(range(cols)):
        for i in reversed(range(j)):
            t_score = 0
            for k in range(i):
                if (mat[i][j] > mat[k][j]):
                    t_score += mat[i][j]-mat[k][j]
            wscore_m[i][j] += t_score
            wscore_m[j][i] += t_score
    return matrix(wscore_m)


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


if __name__ == '__main__':
    structure = {'nb_candidates': 5,
                 'preferences': [(1, [5, 3, 2, 4, Set([1])]), (4, [2, 4, Set([1, 3, 5])]), (1, [3, 5, 4, Set([1])])],
                 'sum_vote_count': 6,
                 'candidates': {1: 'Candidate 1', 2: 'Candidate 2', 3: 'Candidate 3', 4: 'Candidate 4', 5: 'Candidate 5'},
                 'nb_unique_orders': 3,
                 'nb_voters': 6}
    mat = create_similarity_matrix(structure)
    print(mat)
    print(get_matrix_score(mat))
    print(get_weighted_matrix_score(mat))