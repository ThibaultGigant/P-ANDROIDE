# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
sys.path.append(getcwd())

class Benchmark(Frame):
    def __init__(self, parent, filenames, candidates, results):
        Frame.__init__(self, parent)
        self.table = None
        self.display_current_table()
        self.pack_elements()

    def display_current_table(self):
        self.table = Label(self, text="first").grid(row=0)

    def pack_elements(self):
        self.table.pack()