from sage.all import matrix


def create_similarity_matrix(structure):
    """
    Creates the similarity matrix between candidates, given the preferences stored in the structure
    :param structure: data extracted from an election file
    :return: similarity matrix
    :rtype: matrix
    """
    pass


def get_matrix_score(mat):
    """
    Calculate matrix gradient score
    :param mat: similarity matrix between candidates
    :type mat: matrix
    :return: matrix gradient score
    :rtype: int
    """
    pass


def find_permutation_naive(structure):
    """
    Calculate the similarity matrix between candidates then finds the permutation maximizing the matrix gradient score
    :param structure: data extracted from an election file
    :return: list of candidates indices = axis of candidates
    :rtype: list
    """
    pass