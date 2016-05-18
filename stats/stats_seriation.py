# -*-coding: utf-8-*-
from os.path import join
import sys
from os import getcwd
import matplotlib.pyplot as plt

sys.path.append(getcwd())

from Data.axesPAndroide import *
from data_gestion.file_gestion import read_file
from algorithms.find_axis_from_file import find_axis_from_structure
from algorithms.similarity_matrix import *


def time_fixed_nb_candidates(filename):
    structure = read_file(join("Data/all/", filename), strict=filename in listFiles)
    functions = [dissimilarity_and_n, dissimilarity_and_or, dissimilarity_over_over]
    times = []

    for i in range(6):
        print "Iteration " + str(i)
        temp = []
        for j in range(10):
            temp.append(find_axis_from_structure(structure, dissimilarity_function=functions[i % 3], weighted=(i / 3 == 1))[0])
        times.append(sum(temp)/float(len(temp)))

    plt.plot(range(6), times, "-o")
    plt.title("Temps d'execution en fonction des mesures de dissimilarite")
    plt.ylabel("Temps d'execution")
    plt.xlabel("Mesure de dissimilarite")
    plt.savefig("Data/test.png")


def time_variable_nb_candidates():
    dico = {}
    for f in listFiles:
        print f
        structure = read_file(join("Data/all", f), strict=True)
        if structure["nb_candidates"] in dico:
            dico[structure["nb_candidates"]].append(
                find_axis_from_structure(structure, dissimilarity_over_over, True)[0])
        else:
            dico[structure["nb_candidates"]] = [find_axis_from_structure(structure, dissimilarity_over_over, True)[0]]

    abscisse = []
    ordonnee = []
    for n in dico.keys():
        abscisse.append(n)
        ordonnee.append(sum(dico[n]) / float(len(dico[n])))

    print abscisse, ordonnee
    plt.plot(abscisse, ordonnee, "-o")
    plt.title("Temps d'execution en fonction du nombre de candidats")
    plt.ylabel("Temps d'execution")
    plt.xlabel("Nombre de candidats")
    plt.savefig("Data/test.png")


if __name__ == '__main__':
    # time_fixed_nb_candidates(listFiles[-2])
    time_variable_nb_candidates()
