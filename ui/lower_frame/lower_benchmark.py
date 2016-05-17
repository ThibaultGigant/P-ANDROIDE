# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import sys
from os import getcwd

from algorithms.b_and_b import bnb, find_axes2

sys.path.append(getcwd())

from algorithms.find_axis_from_file import find_axis_from_structure
from algorithms.similarity_matrix import *
from data_gestion.file_gestion import read_file
from Data.axesPAndroide import listFiles


class Benchmark(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.files = self.parent.upper_frame.right_frame.list_files
        self.display_table()

    def display_table(self):
        algo = self.parent.upper_frame.left_frame.algo.get()
        weighted = self.parent.upper_frame.left_frame.weighted.get()
        dissimilarity_var = self.parent.upper_frame.left_frame.dissimilarity.get()

        if dissimilarity_var == 0:
            dissimilarity = dissimilarity_and_n
        elif dissimilarity_var == 1:
            dissimilarity = dissimilarity_and_or
        else:
            dissimilarity = dissimilarity_over_over

        # Horizontal and Vertical separators
        ttk.Separator(self, orient=HORIZONTAL).grid(row=0, columnspan=16, sticky="ew")
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=0, rowspan=len(self.files) * 2 + 3, padx=(0, 10),
                                                  sticky="ns")

        # Horizontal labels with separators
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=2, rowspan=len(self.files) * 2 + 3, padx=10,
                                                  sticky="ns")
        Label(self, text="Bulletins").grid(row=1, column=3)
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=4, rowspan=len(self.files) * 2 + 3, padx=10,
                                                  sticky="ns")
        Label(self, text="Bulletins uniques").grid(row=1, column=5)
        ttk.Separator(self, orient=VERTICAL).grid(row=0, column=6, rowspan=len(self.files) * 2 + 3, padx=10,
                                                  sticky="ns")
        if algo == 0:
            Label(self, text="Bulletins (uniques) sélectionnés").grid(row=1, column=7)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=8, rowspan=len(self.files) * 2 + 3, padx=10,
                                                      sticky="ns")
            Label(self, text="Bulletins sélectionnés").grid(row=1, column=9)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=10, rowspan=len(self.files) * 2 + 3, padx=10,
                                                      sticky="ns")
            Label(self, text="Proportion").grid(row=1, column=11)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=12, rowspan=len(self.files) * 2 + 3, padx=10,
                                                      sticky="ns")
            Label(self, text="Axes trouvés").grid(row=1, column=13)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=14, rowspan=len(self.files) * 2 + 3, padx=10,
                                                      sticky="ns")
            Label(self, text="Durée d'exécution").grid(row=1, column=15, padx=(0, 10))
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=16, rowspan=len(self.files) * 2 + 3, sticky="ns")
        else:
            Label(self, text="Axes trouvés").grid(row=1, column=7)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=8, rowspan=len(self.files) * 2 + 3, padx=10,
                                                      sticky="ns")
            Label(self, text="Durée d'exécution").grid(row=1, column=9)
            ttk.Separator(self, orient=VERTICAL).grid(row=0, column=10, rowspan=len(self.files) * 2 + 3, padx=(10, 0),
                                                      sticky="ns")

        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, columnspan=16, sticky="ew")

        # Vertical file names
        vrow = 3
        for f in self.files:
            Label(self, text=f).grid(row=vrow, column=1)
            ttk.Separator(self, orient=HORIZONTAL).grid(row=vrow + 1, columnspan=16, sticky="ew")
            if algo == 0:
                calculate_bnb(self, f, vrow, dissimilarity, weighted)
            else:
                calculate_seriation(self, f, vrow, dissimilarity, weighted)
            vrow += 2

    def destroy_elements(self):
        return


def calculate_bnb(self, file, vrow, dissimilarity, weighted):
    structure = read_file("Data/all/" + str(file), file in listFiles)
    preferences = structure["preferences"]
    candidates = structure["candidates"]
    Label(self, text=str(structure["nb_voters"])).grid(row=vrow, column=3)
    Label(self, text=str(structure["nb_unique_orders"])).grid(row=vrow, column=5)
    t1 = time()
    ensemble, best = bnb(len(preferences), preferences, candidates)
    t2 = time()
    Label(self, text=str(len(best[0][0]))).grid(row=vrow, column=7)
    Label(self, text=str(best[1])).grid(row=vrow, column=9)
    Label(self, text=str(best[1] * 100.0 / structure["nb_voters"])).grid(row=vrow, column=11)
    axes, card = find_axes2(best[0][0], candidates)

    Label(self, text=str(len(axes))).grid(row=vrow, column=13)
    Label(self, text=str(t2 - t1)).grid(row=vrow, column=15)


def calculate_seriation(self, file, vrow, dissimilarity, weighted):
    structure = read_file("Data/all/" + str(file), file in listFiles)
    Label(self, text=str(structure["nb_voters"])).grid(row=vrow, column=3)
    Label(self, text=str(structure["nb_unique_orders"])).grid(row=vrow, column=5)
    if file in listFiles:
        t, axes = find_axis_from_structure(structure, dissimilarity, weighted)
    else:
        t, axes = find_axis_from_structure(structure, dissimilarity, weighted, unwanted_candidates=[2, 3, 7, 11])
    Label(self, text=str(len(axes[1]))).grid(row=vrow, column=7)
    Label(self, text=str(t)).grid(row=vrow, column=9)
