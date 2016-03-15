from axesPAndroide import *
from file_gestion import read_file
from find_axis_from_file import find_axis_from_structure
from similarity_matrix import *
from os.path import join


def get_matches(axis):
    """
    Returns the index of the group where the candidate is, for each candidate
    :param axis: axis in which the search is done
    :return: index of the group where the candidate is, for each candidate
    :rtype: dict[int, int]
    """
    res = {}
    for i in range(len(axis)):
        for candidate in axis[i]:
            res[candidate] = i+1
    return res


def axes_to_latex_graph(filename, axis, name=None,
                        dissimilarity_function=dissimilarity_over_over, weighted=False, strict=False):
    """
    Returns the LaTeX code to display the axis
    :param filename: relative path to the election data file
    :param axis: axis corresponding to the file, according to wikipedia
    :param name: name that will be given to the figures
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param strict: True if the file depicts strict preferences, False otherwise
    :return: string containing the LaTeX code
    """
    structure = read_file(filename, strict)
    t, permutations = find_axis_from_structure(structure, dissimilarity_function, weighted)
    matches = get_matches(axis)
    length_unit = str(len(matches) + 2)
    res = "\\begin{center}\n"

    for permutation in permutations[1]:
        # beginning of the environment
        res += "\\begin{figure}\n"
        res += "\\begin{tikzpicture}[x=\\textwidth/" + length_unit + ", y=\\textwidth/" + length_unit + "]\n"
        # Adding the x and y axes
        res += "\\draw[->, >=latex] (0,0) -- (" + length_unit + ",0);\n"
        res += "\\draw[->, >=latex] (0,0) -- (0," + length_unit + ");\n"
        # Adding the legend below the x axis
        for i in range(len(permutation)):
            res += "\\draw (" + str(i+1) + ",-0.1) node[below] {" + str(permutation[i]) + "};\n"

        res += "\\draw plot[ultra thick]coordinates{"
        temp = ""  # string for the circles marking the dots
        for i in range(len(permutation)):
            if permutation[i] in matches:
                res += "(" + str(i+1) + "," + str(matches[permutation[i]]) + ")"
                temp += "\\draw[fill=black] (" + str(i+1) + "," + str(matches[permutation[i]]) + ") circle (0.1);\n"
        res += "};\n"
        res += temp  # ading the circles
        res += "\\end{tikzpicture}\n"
        if name:
            res += "\\caption{Permutation " + str(permutations[1].index(permutation)) + " of " + name + "}\n"
        res += "\\end{figure}\n"

    res += "\\end{center}\n\\clearpage\n"

    return res


def all_files_to_latex(directory, files_list, axes_list, names_list,
                       dissimilarity_function=dissimilarity_over_over, weighted=False, strict=None):
    """
    Returns a string with all graphics from a list of files
    :param directory: path to the directory where all the files in files_list are
    :param files_list: list of files
    :param axes_list: axes corresponding to the files
    :param names_list: names to give to the figures, for instance the wards corresponding to the elections
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param strict: list of booleans, True if the corresponding file in the list is depicting strict preferences
    :return: LaTeX code to display the graphs corresponding to all the files
    """
    if not strict:
        strict = [False] * len(files_list)
    res = ""
    for i in range(len(files_list)):
        print(files_list[i])
        res += axes_to_latex_graph(join(directory, files_list[i]), axes_list[i], names_list[i],
                                   dissimilarity_function, weighted, strict[i])
    return res


if __name__ == '__main__':
    # s = axes_to_latex_graph(join("Data/glasgow", listFiles[0]), listAxes[0], name=listWards[0])
    # print(s)
    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, strict=[True]*len(listFiles))

    fp = open("Data/TeX/sortie.tex", "w")
    fp.write(s)
    fp.close()

