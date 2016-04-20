# -*- coding: utf-8 -*-
from Tkinter import *


class AlgoMenu(Frame):
    """
    Class displaying all widgets allowing to choose the algorithm to launch
    """
    def __init__(self, master):
        Frame.__init__(self, master, width=500, height=200)
        self.parent = master
        self.algo = IntVar()
        self.dissimilarity = IntVar()
        self.weighted = BooleanVar()
        self.dissimilarity.set(2)
        self.weighted.set(True)
        self.frame_algos = None
        self.frame_params = None
        self.launch_btn = None
        self.add_widgets()

    def add_widgets(self):
        """
        Adds all widgets relative to algorithms
        """
        self.frame_choice_algo()
        self.frame_seriation_parameters()
        self.add_launch_btn()

    def frame_choice_algo(self):
        """
        Adds a LabelFrame to choose the algorithm to launch
        :return:
        """
        # Variable initialization
        self.frame_algos = LabelFrame(self, text="Choose Algorithm")
        self.algo.set(1)

        # Widgets declaration
        label_algo = Label(self.frame_algos, text="Choose the algorithm to launch:", font=("", 16))
        radio_bnb = Radiobutton(self.frame_algos, text="Branch & Bound", variable=self.algo, value=0)
        radio_seriation = Radiobutton(self.frame_algos, text="Seriation", variable=self.algo, value=1)

        # Widgets display
        label_algo.grid(row=0, column=0, columnspan=3)
        radio_bnb.grid(row=1, column=0, columnspan=3, sticky=W)
        radio_seriation.grid(row=2, column=0, columnspan=3, sticky=W)

        self.algo.trace("w", lambda name, index, mode: self.enable_or_disable())
        self.frame_algos.pack()

    def frame_seriation_parameters(self):
        """
        Adds widgets to choose parameters
        :return:
        """
        # Variables declaration
        self.frame_params = LabelFrame(self, text="Parameters for Seriation")

        # Widgets declaration
        label_dissimilarity = Label(self.frame_params, text="Choose the function used to calculate the dissimilarity matrix:",
                                    font=("", 14))
        radio_and_n = Radiobutton(self.frame_params, text="Both candidates over all ballots", variable=self.dissimilarity, value=0)
        radio_and_or = Radiobutton(self.frame_params, text="Both candidates over ballots with one or the other",
                                   variable=self.dissimilarity, value=1)
        radio_over_over = Radiobutton(self.frame_params,
                                      text="Sum of inverse number of ballots with both candidates over sum of inverse number of ballots with one or the other",
                                      variable=self.dissimilarity, value=2)
        label_weighted = Label(self.frame_params, text="Weighted calculation :", font=("", 12))
        radio_weighted = Radiobutton(self.frame_params, text="Weighted", variable=self.weighted, value=True)
        radio_unweighted = Radiobutton(self.frame_params, text="Not Weighted", variable=self.weighted, value=False)

        # Widgets display
        label_dissimilarity.grid(row=0, column=0, columnspan=3, padx=10)
        radio_and_n.grid(row=1, column=0, columnspan=3, sticky=W, padx=10)
        radio_and_or.grid(row=2, column=0, columnspan=3, sticky=W, padx=10)
        radio_over_over.grid(row=3, column=0, columnspan=3, sticky=W, padx=10)
        label_weighted.grid(row=4, column=0, padx=10)
        radio_weighted.grid(row=4, column=1)
        radio_unweighted.grid(row=4, column=2)

        self.frame_params.pack(padx=10)

    def add_launch_btn(self):
        """
        Adds a button to launch the choosed algorithm with right parameters
        """
        self.launch_btn = Button(self, text="Launch Algorithm", command=self.launch)
        self.launch_btn.pack()

    def launch(self):
        """
        Launch the algorithm with the files and options the user selected
        """
        if self.algo == 0:
            pass
        else:
            pass

    def enable_or_disable(self):
        """
        Enables the choice for a dissimilarity function and a weighted calculation if seriation algorithm selected
        Disables them otherwise
        """
        if self.algo.get() == 0:
            self.frame_params.destroy()
            self.frame_params = None
        else:
            self.launch_btn.destroy()
            self.frame_seriation_parameters()
            self.add_launch_btn()
