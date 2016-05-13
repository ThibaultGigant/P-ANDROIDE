# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import sys
from os import getcwd
sys.path.append(getcwd())

class Benchmark(Frame):
    def __init__(self, parent, filenames, candidates, results):
        Frame.__init__(self, parent)
        self.display_table()
        self.files = self.parent.upper_frame.right_frame_list_files

    def display_table(self):
        # Horizontal
        Separator(self,orient=HORIZONTAL).grid(row=0, columnspan=10, sticky="ew")

        Separator(self,orient=VERTICAL).grid(rowspan=10, column=1, padx=10, sticky="ns")
        Label(self, text="Nombre de bulletins").grid(row=1, column=2)
        Separator(self,orient=VERTICAL).grid(rowspan=10, column=3, padx=10, sticky="ns")
        Label(self, text="Nombre d'axes trouvés").grid(row=1, column=4)

        Separator(self,orient=HORIZONTAL).grid(row=2, columnspan=10, sticky="ew")

        vrow = 2
        #Vertical
        #for f in self.list_files:
        #    Label(self, text=f)
        Label(self, text="ED-000.toc").grid(row=3, column=0)

        print(self.files)
