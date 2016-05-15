#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

import sys
from os import getcwd
sys.path.append(getcwd())

from sage.all import Set, matrix
from itertools import permutations, combinations
from data_gestion.generation import generation
from time import time


def dissimilarity_and_n(structure, candidate1, candidate2):
    """
    Calculates the dissimilarity between candidate1 and candidate2 like this:
    1 - number_of_ballots_with_candidate1_AND_candidate2/total_number_of_ballots
    :param structure: data extracted from an election file
    :param candidate1: ID of a candidate
    :param candidate2: ID of a candidate
    :return: dissimilarity score
    :rtype: int
    """
    # if the candidates are identical, their dissimilarity is 0, nothing else to do
    if candidate1 == candidate2:
        return 0

    # Variables initialization
    ballots = structure["preferences"]
    vote_count = float(structure["sum_vote_count"])
    score = 0
    # Calculating number of ballots with the 2 candidates
    for ballot in ballots:
        if candidate1 in ballot[1] and candidate2 in ballot[1]:
            score += ballot[0]

    return 1 - score / vote_count


def dissimilarity_and_or(structure, candidate1, candidate2):
    """
    Calculates the dissimilarity between candidate1 and candidate2 like this:
    1 - number_of_ballots_with_candidate1_AND_candidate2/number_of_ballots_with_candidate1_OR_candidate2
    :param structure: data extracted from an election file
    :param candidate1: ID of a candidate
    :param candidate2: ID of a candidate
    :return: dissimilarity score
    :rtype: int
    """
    # if the candidates are identical, their dissimilarity is 0, nothing else to do
    if candidate1 == candidate2:
        return 0

    # Variables initialization
    ballots = structure["preferences"]
    score = 0
    nb_cand1_or_cand2 = 0
    # Calculating number of ballots with the 2 candidates
    for ballot in ballots:
        if candidate1 in ballot[1] and candidate2 in ballot[1]:
            score += ballot[0]
        if candidate1 in ballot[1] or candidate2 in ballot[1]:
            nb_cand1_or_cand2 += ballot[0]

    return 1 - score / float(nb_cand1_or_cand2)


def dissimilarity_over_over(structure, candidate1, candidate2):
    """
    Calculates the dissimilarity between candidate1 and candidate2 like this:
    1 - sum(1/|ballot_with_candidate1_and_candidate2| * number_of_ballots_with_candidate1_AND_candidate2)/sum(1/|ballot_with_candidate1_OR_candidate2| * number_of_ballots_with_candidate1_OR_candidate2)
    :param structure: data extracted from an election file
    :param candidate1: ID of a candidate
    :param candidate2: ID of a candidate
    :return: dissimilarity score
    :rtype: int
    """
    # if the candidates are identical, their dissimilarity is 0, nothing else to do
    if candidate1 == candidate2:
        return 0

    # Variables initialization
    ballots = structure["preferences"]
    score = 0
    nb_cand1_or_cand2 = 0
    # Calculating number of ballots with the 2 candidates
    for ballot in ballots:
        n = len(ballot[1]) if type(ballot[1][-1]) == int else len(ballot[1]) - 1  # number of candidates approved in the ballot
        if candidate1 in ballot[1] and candidate2 in ballot[1]:
            score += ballot[0] / float(n)
        if candidate1 in ballot[1] or candidate2 in ballot[1]:
            nb_cand1_or_cand2 += ballot[0] / float(n)

    return 1 - score / float(nb_cand1_or_cand2)


def create_similarity_matrix(structure, dissimilarity_function):
    """
    Creates the similarity matrix between candidates, given the preferences stored in the structure
    :param structure: data extracted from an election file
    :type structure: dict
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :type dissimilarity_function: function pointer
    :return: similarity matrix
    :rtype: matrix
    """
    # Variables initialization
    nb_candidates = structure["nb_candidates"]
    similarity_m = [[0 for _ in range(nb_candidates)] for _ in range(nb_candidates)]
    pairs_of_candidates = list(combinations(structure["candidates"].keys(), 2))

    for candidate1, candidate2 in pairs_of_candidates:
        similarity = dissimilarity_function(structure, candidate1, candidate2)
        similarity_m[candidate1 - 1][candidate2 - 1] = similarity
        similarity_m[candidate2 - 1][candidate1 - 1] = similarity

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
    for i in range(rows - 1):
        for j in range(i + 1, cols - 1):
            for k in range(j + 1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    score_m += 1
                # per column
                if mat[rows-j - 1][cols-i - 1] > mat[rows-k - 1][cols-i - 1]:
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
    for i in range(rows - 1):
        for j in range(i + 1, cols - 1):
            for k in range(j + 1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    wscore_m += mat[i][j] - mat[i][k]
                # per column
                if mat[rows-j - 1][cols-i - 1] > mat[rows-k - 1][cols-i - 1]:
                    wscore_m += mat[rows-j - 1][cols-i - 1] > mat[rows-k - 1][cols-i - 1]

    return wscore_m


def find_permutation_naive(similarity_matrix, weighted=False):
    """
    Calculate the similarity matrix between candidates then finds the permutation maximizing the matrix gradient score
    by testing all possible permutation
    :param similarity_matrix: similarity matrix between candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :type weighted: bool
    :return: list of candidates indices = axis of candidates
    :rtype: list
    """
    # Variables initialization
    nb_candidates = similarity_matrix.nrows()
    candidates_id = range(nb_candidates)
    candidates_permutations = list(permutations(candidates_id, nb_candidates))

    # We can work only on the first half of the permutations, the other ones are symetric
    # candidates_permutations = candidates_permutations[:len(candidates_permutations) / 2]

    # Calculating scores for all possible permutations
    if weighted:
        score = get_weighted_matrix_score(
            similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[0]),
                                                           list(candidates_permutations[0])))
    else:
        score = get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[0]),
                                                                                list(candidates_permutations[0])))
    optimal_permutations = [candidates_permutations[0]]
    for i in range(1, len(candidates_permutations)):
        if weighted:
            temp = get_weighted_matrix_score(
                similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[i]),
                                                               list(candidates_permutations[i])))
        else:
            temp = get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[i]),
                                                                                   list(candidates_permutations[i])))
        if temp < score:
            score = temp
            optimal_permutations = [candidates_permutations[i]]
        elif temp == score:
            optimal_permutations.append(candidates_permutations[i])

    return [[i+1 for i in permutation] for permutation in optimal_permutations]


def get_distance_score(mat, candidate_index):
    """
    Calculates matrix gradient score from a candidate
    :param mat: similarity matrix between candidates
    :param candidate_index: index of the candidate to be compared to the others, in the similarity matrix
    :type mat: matrix
    :type candidate_index: int
    :return: matrix gradient score
    :rtype: int
    """
    cols = mat.ncols()
    score_m = 0

    # Calculates score
    for line in range(candidate_index):
        for col in range(candidate_index + 1, cols):
            # per row
            if mat[line][candidate_index] > mat[line][col]:
                score_m += 1

            # per column
            if mat[candidate_index][col] > mat[line][col]:
                score_m += 1

    return score_m


def get_weighted_distance_score(mat, candidate_index):
    """
    Calculates matrix's weighted gradient score from a candidate
    :param mat: similarity matrix between candidates
    :param candidate_index: index of the candidate to be compared to the others, in the similarity matrix
    :type mat: matrix
    :type candidate_index: int
    :return: matrix gradient score
    :rtype: int
    """
    cols = mat.ncols()
    score_m = 0

    # Calculates score
    for line in range(candidate_index):
        for col in range(candidate_index + 1, cols):
            # per row
            if mat[line][candidate_index] > mat[line][col]:
                score_m += mat[line][candidate_index] - mat[line][col]

            # per column
            if mat[candidate_index][col] > mat[line][col]:
                score_m += mat[candidate_index][col] - mat[line][col]

    return score_m


def distance(similarity_matrix, candidates_set, candidate, function_map, weighted=False):
    """
    Calculatest the "distance" between a set of candidates and a given candidate,
    by adding the dissimilarity between each candidate in the set and the given candidate
    :param similarity_matrix: similarity matrix between candidates
    :param candidates_set: set of candidates
    :param candidate: candidate to be compared to the others
    :param function_map: map whose keys are sets of candidates and values are a tuple (score, optimal permutation so far)
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :type similarity_matrix: matrix
    :type candidates_set: Set
    :type candidate: int
    :type function_map: dict
    :type weighted: bool
    :return: "distance" between the set of candidates and the given candidate
    :rtype: list
    """
    candidates_permutations = [[i - 1 for i in j] + [candidate - 1] for j in function_map[candidates_set][1]]
    candidates_permutations = [j + [i for i in range(similarity_matrix.nrows()) if i not in j] for j in
                               candidates_permutations]

    if weighted:
        scores = [(get_weighted_distance_score(similarity_matrix.matrix_from_rows_and_columns(i, i),
                                               candidates_set.cardinality()),
                   [j + 1 for j in i[:candidates_set.cardinality() + 1]]) for i in candidates_permutations]
    else:
        scores = [(get_distance_score(similarity_matrix.matrix_from_rows_and_columns(i, i),
                                      candidates_set.cardinality()),
                   [j + 1 for j in i[:candidates_set.cardinality() + 1]]) for i in candidates_permutations]

    minimum = min(scores, key=lambda x: x[0])
    return [score for score in scores if score[0] == minimum[0]]


def find_permutation_dynamic_programming(similarity_matrix, candidates_set, function_map, weighted=False):
    """
    Finds the permutation maximizing the gradient score with a dynamic programming algorithm
    :param similarity_matrix: similarity matrix between candidates
    :param candidates_set: set of candidates used on this iteration
    :param function_map: map whose keys are sets of candidates and values are a tuple (score, optimal permutations so far)
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :type similarity_matrix: matrix
    :type candidates_set: Set
    :type function_map: dict
    :type weighted: bool
    :return: map of sets of candidates and tuple, containing the optimal permutation
    :rtype: dict
    """
    # If it has already been calculated, just return the result
    if candidates_set in function_map:
        return function_map

    # else if it has only one element, the score is 0 and the optimal permutation is a 1-element list
    if candidates_set.cardinality() == 1:
        function_map[candidates_set] = (0, [[candidates_set.an_element()]])
        return function_map

    # else, recursive call on all combinations
    candidates_combinations = list(combinations(candidates_set, candidates_set.cardinality() - 1))
    temp = []
    for combination in candidates_combinations:
        comb = Set(combination)
        current_candidate = candidates_set.symmetric_difference(comb).an_element()
        function_map = find_permutation_dynamic_programming(similarity_matrix, comb, function_map, weighted)  # recursive call

        scores = distance(similarity_matrix, comb, current_candidate, function_map, weighted)
        for score in scores:
            temp.append((score[1], score[0] + function_map[comb][0]))

    minimum = min(temp, key=lambda x: x[1])  # tuple with the minimum score of this iteration
    minimums = [i for i in temp if i[1] == minimum[1]]  # keep all combinations giving the minimum score
    # print("taille liste minimums : " + str(len(minimums)))

    function_map[candidates_set] = (minimum[1], [i for i, j in minimums])
    # print ("temp : " + str(temp))

    return function_map


################################################
# Functions used in development, to remove !!! #
################################################
def example1():
    structure, axis = generation(7, 10000, 3)
    print("Generated axis: " + str(axis))
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_over_over)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: " + str(get_matrix_score(mat)))
    print("Weighted Gradient score: " + str(get_weighted_matrix_score(mat)))

    t = time()
    dico = find_permutation_dynamic_programming(mat, Set(structure["candidates"].keys()), {})
    t = time() - t
    print("Dynamic programming algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(dico[Set(structure["candidates"].keys())][1]))

    t = time()
    optimal_permutation = find_permutation_naive(mat)
    t = time() - t
    print("Naive algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(optimal_permutation))


def example2():
    structure, axis = generation(7, 10000, 3)
    print("Generated axis: " + str(axis))
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_over_over)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: " + str(get_matrix_score(mat)))
    print("Weighted Gradient score: " + str(get_weighted_matrix_score(mat)))

    t = time()
    dico = find_permutation_dynamic_programming(mat, Set(structure["candidates"].keys()), {}, weighted=True)
    t = time() - t
    print("Dynamic programming algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(dico[Set(structure["candidates"].keys())][1]))

    t = time()
    optimal_permutation = find_permutation_naive(mat)
    t = time() - t
    print("Naive algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(optimal_permutation))


def example3():
    mat = matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: " + str(get_matrix_score(mat)))
    print("Weighted Gradient score: " + str(get_weighted_matrix_score(mat)))

    t = time()
    dico = find_permutation_dynamic_programming(mat, Set([1, 2, 3, 4]), {}, weighted=True)
    t = time() - t
    print("Dynamic programming algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(dico[Set(Set([1, 2, 3, 4]))][1]))

    t = time()
    optimal_permutation = find_permutation_naive(mat)
    t = time() - t
    print("Naive algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(optimal_permutation))


def example4():
    mat = matrix([[0, 1, 4, 5], [1, 0, 3, 4], [4, 3, 0, 1], [5, 4, 1, 0]])
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: " + str(get_matrix_score(mat)))
    print("Weighted Gradient score: " + str(get_weighted_matrix_score(mat)))

    t = time()
    dico = find_permutation_dynamic_programming(mat, Set([1, 2, 3, 4]), {}, weighted=True)
    t = time() - t
    print("Dynamic programming algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(dico[Set(Set([1, 2, 3, 4]))][1]))

    t = time()
    optimal_permutation = find_permutation_naive(mat)
    t = time() - t
    print("Naive algorithm: " + str(t) + "seconds")
    print("Optimal permutations: " + str(optimal_permutation))


if __name__ == '__main__':
    # example1()
    example2()
    # example3()
    # example4()
