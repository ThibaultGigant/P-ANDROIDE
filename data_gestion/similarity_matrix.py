#! /usr/bin/env sage -python
# -*- coding: utf-8 -*-

from sage.all import Set, matrix
from itertools import permutations, combinations
from generation import generation
from file_gestion import read_file
from time import time
import sys


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

    return 1-score/vote_count


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

    return 1-score/float(nb_cand1_or_cand2)


def dissimilarity_over_over(structure, candidate1, candidate2):
    """
    Calculates the dissimilarity between candidate1 and candidate2 like this:
    1 - sum(1/|ballot_with_candidate1_and_candidate2|)/sum(1/|ballot_with_candidate1_OR_candidate2|)
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
            score += 1.0/ballot[0]
        if candidate1 in ballot[1] or candidate2 in ballot[1]:
            nb_cand1_or_cand2 += 1.0/ballot[0]

    return 1-score/float(nb_cand1_or_cand2)


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
        similarity_m[candidate1-1][candidate2-1] = similarity
        similarity_m[candidate2-1][candidate1-1] = similarity

    return matrix(similarity_m)


def get_matrix_score(mat, _from=0):
    """
    Calculates matrix gradient score
    :param mat: similarity matrix between candidates
    :param _from: index of line and column from where to start the counting
    :type mat: matrix
    :type _from: int
    :return: matrix gradient score
    :rtype: int
    """
    rows = mat.nrows()
    cols = mat.ncols()
    score_m = 0

    # Calculates score
    for i in range(_from, rows):
        for j in range(i, cols-1):
            for k in range(j+1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    score_m += 1
                # per column
                if mat[-i-1][-j-1] > mat[-i-1][-k-1]:
                    score_m += 1

    return score_m


def get_weighted_matrix_score(mat, _from=0):
    """
    Calculates the matrix's weighted gradient score
    :param mat: similarity matrix between candidates
    :param _from: index of line and column from where to start the counting
    :type mat: matrix
    :type _from: int
    :return: weighted gradient score
    :rtype: int
    """
    rows = mat.nrows()
    cols = mat.ncols()
    wscore_m = 0

    # Calculates score
    for i in range(_from, rows):
        for j in range(i, cols-1):
            for k in range(j+1, cols):
                # per row
                if mat[i][j] > mat[i][k]:
                    wscore_m += mat[i][j] - mat[i][k]
                # per column
                if mat[-i-1][-j-1] > mat[-i-1][-k-1]:
                    wscore_m += mat[-i-1][-j-1] - mat[-i-1][-k-1]

    return wscore_m


def find_permutation_naive(structure, dissimilarity_function, weighted=False):
    """
    Calculate the similarity matrix between candidates then finds the permutation maximizing the matrix gradient score
    by testing all possible permutation
    :param structure: data extracted from an election file
    :param dissimilarity_function: function used to calculate the dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :type weighted: bool
    :return: list of candidates indices = axis of candidates
    :rtype: list
    """
    # Variables initialization
    candidates_id = range(structure["nb_candidates"])
    candidates_permutations = list(permutations(candidates_id, structure["nb_candidates"]))
    similarity_matrix = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_function)

    t = time()

    candidates_permutations = candidates_permutations[:len(candidates_permutations)/2]

    # Calculating scores for all possible permutations
    if weighted:
        score = get_weighted_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[0]), list(candidates_permutations[0])))
    else:
        score = get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[0]), list(candidates_permutations[0])))
    optimal_permutation = candidates_permutations[0]
    for i in range(1, len(candidates_permutations)):
        if weighted:
            temp = get_weighted_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[i]), list(candidates_permutations[i])))
        else:
            temp = get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(list(candidates_permutations[i]), list(candidates_permutations[i])))
        if temp < score:
            score = temp
            optimal_permutation = candidates_permutations[i]

    t = time() - t
    print("Naive algorithm: " + str(t) + "seconds")
    print("Optimal permutation: " + str([i+1 for i in optimal_permutation]))
    print("Similarity matrix after permutation:")

    return optimal_permutation


def distance(similarity_matrix, candidates_set, candidate, function_map, weighted=False):
    """
    Calculatest the "distance" between a set of candidates and a given candidate,
    by adding the dissimilarity between each candidate in the set and the given candidate
    :param similarity_matrix: similarity matrix between candidates
    :param candidates_set: set of candidates
    :param candidate: candidate to be compared to the others
    :param function_map: map whose keys are sets of candidates and values are a tuple (score, optimal permutation so far)
    :type similarity_matrix: matrix
    :type candidates_set: Set
    :type candidate: int
    :type function_map: dict
    :return: "distance" between the set of candidates and the given candidate
    :rtype: float
    """
    candidates_permutations = [[i-1 for i in j] + [candidate-1] for j in function_map[candidates_set][1]]
    candidates_permutations = [j + [i for i in range(similarity_matrix.nrows()) if i not in j] for j in candidates_permutations]

    if weighted:
        scores = [(get_weighted_matrix_score(similarity_matrix.matrix_from_rows_and_columns(i, i)), i[:candidates_set.cardinality() + 1]) for i in candidates_permutations]
    else:
        scores = [(get_matrix_score(similarity_matrix.matrix_from_rows_and_columns(i, i)), i[:candidates_set.cardinality() + 1]) for i in candidates_permutations]

    minimum = min(scores, key=lambda x: x[0])
    return [(i, [k+1 for k in j]) for i, j in scores if i == minimum[0]]


def find_permutation_dynamic_programming(similarity_matrix, candidates_set, function_map):
    """
    Finds the permutation maximizing the gradient score with a dynamic programming algorithm
    :param similarity_matrix: similarity matrix between candidates
    :param candidates_set: set of candidates used on this iteration
    :param function_map: map whose keys are sets of candidates and values are a tuple (score, optimal permutation so far)
    :type similarity_matrix: matrix
    :type candidates_set: Set
    :type function_map: dict
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
    candidates_combinations = list(combinations(candidates_set, candidates_set.cardinality()-1))
    temp = []
    for combination in candidates_combinations:
        comb = Set(combination)
        current_candidate = candidates_set.symmetric_difference(comb).an_element()
        function_map = find_permutation_dynamic_programming(similarity_matrix, comb, function_map)  # recursive call

        scores = distance(similarity_matrix, comb, current_candidate, function_map)
        # score = function_map[comb][0] + distance(similarity_matrix, comb, current_candidate, function_map)
        for score in scores:
            temp.append((score[1], score[0] + function_map[comb][0]))
        # temp.append((comb, current_candidate, score))

    minimum = min(temp, key=lambda x: x[1])  # tuple with the minimum score of this iteration
    minimums = [i for i in temp if i[1] == minimum[1]]  # keep all combinations giving the minimum score

    function_map[candidates_set] = (minimum[1], [i for i, j in minimums])

    return function_map


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
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_and_or)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    optimal_permutation = find_permutation_naive(structure, dissimilarity_and_or)
    print("Optimal permutation: ", optimal_permutation)
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example2():
    structure = generation(7, 20)
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_and_or)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    optimal_permutation = find_permutation_naive(structure, dissimilarity_and_or)
    print("Optimal permutation: ", [i+1 for i in optimal_permutation])
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example3():
    structure = generation(7, 20)
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_over_over)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    optimal_permutation = find_permutation_naive(structure, dissimilarity_over_over, weighted=True)
    print("Optimal permutation: ", [i+1 for i in optimal_permutation])
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example4():
    structure = generation(7, 10000, 3)
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_over_over)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    t = time()
    optimal_permutation = find_permutation_naive(structure, dissimilarity_over_over)
    t = time() - t
    print(t, "seconds")
    print("Optimal permutation: ", [i+1 for i in optimal_permutation])
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example5():
    if len(sys.argv) != 2:
        raise IOError("This program takes one and only one argument, an election file")
    file = sys.argv[1]
    structure = read_file(file)
    mat = create_similarity_matrix(structure, dissimilarity_function=dissimilarity_and_or)
    print("Similarity Matrix")
    print(mat)
    print("Gradient score: ", get_matrix_score(mat))
    print("Weighted Gradient score: ", get_weighted_matrix_score(mat))

    t = time()
    optimal_permutation = find_permutation_naive(structure, dissimilarity_and_or)
    t = time() - t
    print(t, "seconds")
    print("Optimal permutation: ", [i+1 for i in optimal_permutation])
    print("Similarity matrix after permutation:")
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


def example6():
    structure, axis = generation(7, 10000, 3)
    print("Generated axis: "+str(axis))
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
    # print("Similarity matrix after permutation:")
    # optimal_permutation = [i-1 for i in dico[Set(structure["candidates"].keys())][1]]
    # print(mat.matrix_from_rows_and_columns(optimal_permutation, optimal_permutation))

    optimal_permutation = find_permutation_naive(structure, dissimilarity_over_over)
    print(mat.matrix_from_rows_and_columns(list(optimal_permutation), list(optimal_permutation)))


if __name__ == '__main__':
    # example1()
    # example2()
    # example3()
    # example4()
    # example5()
    example6()
