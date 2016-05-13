# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import sys
from os import getcwd

from algorithms.find_axis_from_file import find_axis_from_structure
from algorithms.similarity_matrix import *
from data_gestion.file_gestion import read_file

sys.path.append(getcwd())

class Benchmark(Frame):
    def __init__(self, parent, filenames, candidates, results):
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
        ttk.Separator(self,orient=HORIZONTAL).grid(row=0, columnspan=13, sticky="ew")
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=0, rowspan=len(self.files)*2+3, padx=(0,10), sticky="ns")
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=12, rowspan=len(self.files)*2+3, padx=(10,0), sticky="ns")

        #Horizontal labels with separators
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=2, rowspan=len(self.files)*2+3, padx=10, sticky="ns")
        Label(self, text="Nb de bulletins").grid(row=1, column=3)
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=4, rowspan=len(self.files)*2+3, padx=10, sticky="ns")
        Label(self, text="Nb de bulletins uniques").grid(row=1, column=5)
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=6, rowspan=len(self.files)*2+3, padx=10, sticky="ns")
        Label(self, text="Nb de bulletins sélectionnés").grid(row=1, column=7)
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=8, rowspan=len(self.files)*2+3, padx=10, sticky="ns")
        Label(self, text="Nb d'axes trouvés").grid(row=1, column=9)
        ttk.Separator(self,orient=VERTICAL).grid(row=0, column=10, rowspan=len(self.files)*2+3, padx=10, sticky="ns")
        Label(self, text="Durée d'exécution").grid(row=1, column=11)

        ttk.Separator(self,orient=HORIZONTAL).grid(row=2, columnspan=13, sticky="ew")

        #Vertical file names
        vrow = 3
        for f in self.files:
            Label(self, text=f).grid(row=vrow, column=1)
            ttk.Separator(self,orient=HORIZONTAL).grid(row=vrow+1, columnspan=13, sticky="ew")
            if algo == 0:
                calculate_bnb(self, f, vrow, dissimilarity, weighted)
            else:
                calculate_seriation(self, f, vrow, dissimilarity, weighted)
            vrow+=2

def calculate_bnb(self, file, vrow, dissimilarity, weighted):
    print("Branch and Bound")

def calculate_seriation(self, file, vrow, dissimilarity, weighted):
    structure = read_file("Data/all/"+str(file))
    Label(self, text=str(structure["nb_voters"])).grid(row=vrow, column=3)
    Label(self, text=str(structure["nb_unique_orders"])).grid(row=vrow, column=5)
    t, axes = find_axis_from_structure(structure, dissimilarity, weighted)
    Label(self, text=str(len(axes[1]))).grid(row=vrow, column=9)
    Label(self, text=str(t)).grid(row=vrow, column=11)


