from os.path import join
import sys
from os import getcwd

sys.path.append(getcwd())

from Data.axesPAndroide import *
from data_gestion.file_gestion import read_file, read_directory
from find_axis_from_file import find_axis_from_structure
from algorithms.b_and_b import bnb, find_axes2
from algorithms.similarity_matrix import *


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


def filter_symmetric_axes(permutations):
    """
    Filter the list of permutations to keep only one axis when 2 are symmetric
    :param permutations: list of permutations found
    :type permutations: list[list[int]]
    :return: the filtered list of permutations
    :rtype: list[list[int]]
    """
    filtered_permutations = []
    for permutation in permutations:
        if list(reversed(permutation)) not in filtered_permutations:
            filtered_permutations.append(permutation)
    return filtered_permutations


def axes_to_latex_graph(structure, axis, name=None,
                        dissimilarity_function=dissimilarity_over_over, weighted=False,
                        unwanted_candidates=[]):
    """
    Returns the LaTeX code to display the axis
    :param structure: structure extracted from a file or directory
    :param axis: axis corresponding to the file, according to wikipedia
    :param name: name that will be given to the figures
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    :return: string containing the LaTeX code
    """
    t, permutations = find_axis_from_structure(structure, dissimilarity_function, weighted, unwanted_candidates)
    permutations = filter_symmetric_axes(permutations[1])
    matches = get_matches(axis)
    length_unit = str(len(permutations[0]) + 1)
    res = "\\section{" + str(name) + "}" if name else ""
    res += "\\begin{center}\n"

    for permutation in permutations:
        # beginning of the environment
        res += "\\begin{figure}\n"
        res += "\\begin{tikzpicture}[x=\\textwidth/" + length_unit + ", y=\\textwidth/" + length_unit + "]\n"
        # Adding the x and y axes
        res += "\\draw[->, >=latex] (0,0) -- (" + length_unit + ",0);\n"
        res += "\\draw[->, >=latex] (0,0) -- (0, 5.5);\n"
        #res += "\\draw[->, >=latex] (0,0) -- (" + length_unit + ",0);\n"
        #res += "\\draw[->, >=latex] (0,0) -- (0," + length_unit + ");\n"
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
            res += "\\caption{Permutation " + str(permutations.index(permutation)) + " of " + name + "}\n"
        res += "\\end{figure}\n"

    res += "\\end{center}\n\\clearpage\n"

    return res

def axes_to_latex_graph_bnb(f, axis, name=None):
    """
    Returns the LaTeX code to display the axis
    :param structure: structure extracted from a file or directory
    :param axis: axis corresponding to the file, according to wikipedia
    :param name: name that will be given to the figures
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param unwanted_candidates: list of candidates to exclude from the search
    :return: string containing the LaTeX code
    """

    structure = read_file(f)
    preferences = structure["preferences"]
    candidates = [i+1 for i in range(len(structure["candidates"]))]
    bb, best = bnb(len(preferences), preferences, candidates)
    permutations, card = find_axes2(best[0][0], candidates)

    matches = get_matches(axis)
    length_unit = str(len(permutations[0]) + 1)
    res = "\\section{" + str(name) + "}" if name else ""
    res += "\\begin{center}\n"

    for permutation in permutations:
        # beginning of the environment
        res += "\\begin{figure}\n"
        res += "\\begin{tikzpicture}[x=\\textwidth/" + length_unit + ", y=\\textwidth/" + length_unit + "]\n"
        # Adding the x and y axes
        res += "\\draw[->, >=latex] (0,0) -- (" + length_unit + ",0);\n"
        res += "\\draw[->, >=latex] (0,0) -- (0, 5.5);\n"
        #res += "\\draw[->, >=latex] (0,0) -- (" + length_unit + ",0);\n"
        #res += "\\draw[->, >=latex] (0,0) -- (0," + length_unit + ");\n"
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
            res += "\\caption{Permutation " + str(permutations.index(permutation)) + " of " + name + "}\n"
        res += "\\end{figure}\n"

    res += "\\end{center}\n\\clearpage\n"

    return res

def all_files_to_latex(directory, files_list, axes_list, names_list,
                       dissimilarity_function=dissimilarity_over_over, weighted=False, strict=None,
                       unwanted_candidates=[]):
    """
    Returns a string with all graphics from a list of files
    :param directory: path to the directory where all the files in files_list are
    :param files_list: list of files
    :param axes_list: axes corresponding to the files
    :param names_list: names to give to the figures, for instance the wards corresponding to the elections
    :param dissimilarity_function: function to use to calculate dissimilarity between 2 candidates
    :param weighted: if True, matrices scores are calculated with the weighted gradient
    :param strict: list of booleans, True if the corresponding file in the list is depicting strict preferences
    :param unwanted_candidates: list of candidates to exclude from the search
    :return: LaTeX code to display the graphs corresponding to all the files
    """
    if not strict:
        strict = [False] * len(files_list)
    res = ""
    for i in range(len(files_list)):
        print(files_list[i])
        structure = read_file(join(directory, files_list[i]), strict[i])
        res += axes_to_latex_graph(structure, axes_list[i], names_list[i],
                                   dissimilarity_function, weighted, unwanted_candidates)
    return res


def launch_irish_glasgow():
    # on Irish and Glasgow data
    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_over_over,
                           weighted=False, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_over_over.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_over_over,
                           weighted=True, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_over_over_weighted.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_and_n,
                           weighted=False, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_and_n.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_and_n,
                           weighted=True, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_and_n_weighted.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_and_or,
                           weighted=False, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_and_or.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFiles, listAxes, listWards, dissimilarity_function=dissimilarity_and_or,
                           weighted=True, strict=[True]*len(listFiles))
    fp = open("Data/TeX/irish_glasgow_and_or_weighted.tex", "w")
    fp.write(s)
    fp.close()

def launch_french():
    # on French data
    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_over_over,
                           weighted=False, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_over_over.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_over_over,
                           weighted=True, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_over_over_weighted.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_and_n,
                           weighted=False, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_and_n.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_and_n,
                           weighted=True, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_and_n_weighted.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_and_or,
                           weighted=False, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_and_or.tex", "w")
    fp.write(s)
    fp.close()

    s = all_files_to_latex("Data/all", listFrenchFiles, listFrenchAxes, listFrenchWards,
                           dissimilarity_function=dissimilarity_and_or,
                           weighted=True, strict=[False]*len(listFiles),
                           unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_and_or_weighted.tex", "w")
    fp.write(s)
    fp.close()


def launch_french_fusion():
    structure = read_directory("Data/frenchapproval")
    functions = [dissimilarity_and_n, dissimilarity_and_or, dissimilarity_over_over]
    names = ["dissimilarity\_and\_n weighted", "dissimilarity\_and\_n not weighted",
             "dissimilarity\_and\_or weighted", "dissimilarity\_and\_or not weighted",
             "dissimilarity\_over\_over weighted", "dissimilarity\_over\_over not weighted"]
    s = ""
    for i in range(6):
        print "Iteration " + str(i)
        s += axes_to_latex_graph(structure, listFrenchAxes[0], names[i], functions[i/2], i % 2 == 0,
                                 unwanted_candidates=[2, 3, 7, 11])
    fp = open("Data/TeX/french_fusion.tex", "w")
    fp.write(s)
    fp.close()

def launch_french_bnb():
    s = axes_to_latex_graph_bnb(sys.argv[1], listFrenchAxes[0], name=str(sys.argv[1]))
    fp = open("results","w")
    fp.write(s)
    fp.close()

if __name__ == '__main__':
    # launch_irish_glasgow()
    # launch_french()
    # launch_french_fusion()
    launch_french_bnb()
