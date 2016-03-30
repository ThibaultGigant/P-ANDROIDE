# -*- coding: utf-8 -*-
from Tkinter import *


class AlgoMenu(Frame):
    """
    Class displaying all widgets allowing to choose the algorithm to launch
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.disabled = []
        self.algo = IntVar()
        self.add_widgets()

    def add_widgets(self):
        """
        Adds all widgets relative to algorithms
        """
        # Variables declaration
        dissimilarity = IntVar()
        weighted = IntVar()
        self.algo.set(1)
        dissimilarity.set(0)
        weighted.set(0)

        # Widgets declaration
        label_algo = Label(self, text="Choose algorithm:", font=("", 16))
        radio_bnb = Radiobutton(self, text="Branch & Bound", variable=self.algo)
        radio_seriation = Radiobutton(self, text="Seriation", variable=self.algo)

        label_dissimilarity = Label(self, text="Choose the function used to calculate the dissimilarity matrix:",
                                    font=("", 14))
        radio_and_n = Radiobutton(self, text="Both candidates over all ballots", variable=dissimilarity)
        radio_and_or = Radiobutton(self, text="Both candidates over ballots with one or the other", variable=dissimilarity)
        radio_over_over = Radiobutton(self, text="Sum of inverse number of ballots with both candidates over sum of inverse number of ballots with one or the other", variable=dissimilarity)
        label_weighted = Label(text="Weighted calculation :", font=("", 14))
        radio_weighted = Radiobutton(self, text="Weighted", variable=weighted)
        radio_unweighted = Radiobutton(self, text="Not Weighted", variable=weighted)
        self.disabled += [label_dissimilarity, radio_and_n, radio_and_or, radio_over_over,
                          label_weighted, radio_weighted, radio_unweighted]

        # Widgets display
        label_algo.grid(row=0, column=0, columnspan=3)
        radio_bnb.grid(row=1, column=0, columnspan=3, sticky=W)
        radio_seriation.grid(row=2, column=0, columnspan=3, sticky=W)

        label_dissimilarity.grid(row=3, column=0, columnspan=3, padx=10)
        radio_and_n.grid(row=4, column=0, columnspan=3, sticky=W, padx=10)
        radio_and_or.grid(row=5, column=0, columnspan=3, sticky=W, padx=10)
        radio_over_over.grid(row=6, column=0, columnspan=3, sticky=W, padx=10)
        label_weighted.grid(row=7, column=0, padx=10)
        radio_weighted.grid(row=7, column=1)
        radio_unweighted.grid(row=7, column=2)

        self.algo.trace("w", self.enable_or_disable)

    def enable_or_disable(self):
        """
        Enables the choice for a dissimilarity function and a weighted calculation if seriation algorithm selected
        Disables them otherwise
        """
        if self.algo == 0:
            for w in self.disabled:
                w.config(state=DISABLED)
        else:
            for w in self.disabled:
                w.config(state=NORMAL)
