# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
from os.path import join
sys.path.append(getcwd())

from algorithms.find_axis_from_file import find_axis_from_structure
from data_gestion.file_gestion import read_file
from Data.axesPAndroide import *
from algorithms.similarity_matrix import dissimilarity_and_n, dissimilarity_and_or, dissimilarity_over_over
from algorithms.display_axes import filter_symmetric_axes, get_matches


def func(x):
    return 2*x


class Interactive(Frame):
    """
    Lower Frame, with the interactive display, showing results for each file
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.left_image = None
        self.right_image = None
        self.label_name = None
        self.left_arrow = None
        self.right_arrow = None
        self.results = []
        self.get_results()
        self.current_graph = 0
        self.graph = None
        self.display_current_graph()
        self.pack_elements()

    def make_left_arrow(self, active):
        """
        Creates a canvas on the left, with a left arrow, whose color depends on the "active" boolean
        :param active: If True, changes the color of the arrow, and it's action
        :type active: bool
        :return: the created canvas
        """
        canvas = Canvas(self, width=100, height=100)
        if active:
            img = PhotoImage(file="ui/lower_frame/images/left_arrow.gif")
        else:
            img = PhotoImage(file="ui/lower_frame/images/left_arrow_inactive.gif")
        self.left_image = img
        canvas.create_image(0, 0, image=img, anchor="nw", tag="leftarrow")
        if active:
            canvas.tag_bind("leftarrow", "<Button-1>", self.display_previous_result)
        return canvas

    def make_right_arrow(self, active):
        """
        Creates a canvas on the left, with a left arrow, whose color depends on the "active" boolean
        :param active: If True, changes the color of the arrow, and it's action
        :type active: bool
        :return: the created canvas
        """
        canvas = Canvas(self, width=100, height=100)
        if active:
            img = PhotoImage(file="ui/lower_frame/images/right_arrow.gif")
        else:
            img = PhotoImage(file="ui/lower_frame/images/right_arrow_inactive.gif")
        self.right_image = img
        canvas.create_image(0, 0, anchor="nw", image=img, tag="rightarrow")
        if active:
            canvas.tag_bind("rightarrow", "<Button-1>", self.display_next_result)
        return canvas

    def display_previous_result(self, event):
        self.current_graph -= 1
        self.display_current_graph()
        self.pack_elements()

    def display_next_result(self, event):
        self.current_graph += 1
        self.display_current_graph()
        self.pack_elements()

    def display_current_graph(self):
        self.destroy_elements()
        self.left_arrow = self.make_left_arrow(self.current_graph > 0)
        self.right_arrow = self.make_right_arrow(self.current_graph < len(self.results)-1)
        result = self.results[self.current_graph]
        if result[0] in listFiles:
            self.label_name = Label(self, text="File name:\n" + result[0] + "\n\nWard name:\n" + listWards[listFiles.index(result[0])])
        elif result[0] in listFrenchFiles:
            self.label_name = Label(self, text="File name:\n" + result[0] + "\n\nWard name:\n" + listFrenchWards[listFrenchFiles.index(result[0])])
        self.graph = Graph(self.results[self.current_graph])
        self.graph.afficher(10)

    def pack_elements(self):
        self.graph.pack()
        self.left_arrow.pack(side=LEFT)
        self.label_name.pack(side=LEFT)
        self.right_arrow.pack(side=RIGHT)

    def destroy_elements(self):
        if self.left_arrow:
            self.left_arrow.destroy()
        if self.right_arrow:
            self.right_arrow.destroy()
        if self.label_name:
            self.label_name.destroy()
        if self.graph:
            self.graph.destroy()

    def get_results(self):
        for f in self.parent.upper_frame.right_frame.list_files:
            structure = read_file(join("Data/all", f), f in listFiles)
            if self.parent.upper_frame.left_frame.algo.get() == 0:
                pass
            else:
                if self.parent.upper_frame.left_frame.dissimilarity.get() == 0:
                    dissimilarity_function = dissimilarity_and_n
                elif self.parent.upper_frame.left_frame.dissimilarity.get() == 1:
                    dissimilarity_function = dissimilarity_and_or
                else:
                    dissimilarity_function = dissimilarity_over_over
                t, permutations = find_axis_from_structure(structure, dissimilarity_function,
                                                           self.parent.upper_frame.left_frame.weighted.get())
                permutations = filter_symmetric_axes(permutations[1])
                for permutation in permutations:
                    self.results.append((f, permutation))


class Graph(Canvas):
    MAX_WIDTH = 800  # taille maxi choisi pour mon écran
    MAX_HEIGHT = 200  # idem

    def __init__(self, result):
        """
        Creates the graph of one of the permutation found for this file
        :param result: tuple (file, permutation) found by the algorithm
        """
        Canvas.__init__(self, width=Graph.MAX_WIDTH+20, height=Graph.MAX_HEIGHT+20)
        self.xmin = 0
        self.xmax = len(result[1]) + 1

        f = result[0]
        permutation = result[1]

        self.file = f
        self.permutation = permutation

        if f in listFiles:
            self.axis = listAxes[listFiles.index(f)]
        else:
            self.axis = listFrenchAxes[listFrenchFiles.index(f)]

        self.ymin = 0
        self.ymax = len(self.axis) + 1

        matches = get_matches(self.axis)

        self.values = []

        for i in range(len(permutation)):
            if permutation[i] in matches:
                self.values.append((permutation[i], i+1, matches[permutation[i]]))

        self.coeffx = (Graph.MAX_WIDTH - 20) / (self.xmax - self.xmin)
        self.coeffy = (Graph.MAX_HEIGHT-20) / (self.ymax - self.ymin)

    def afficher(self, diametre):
        zerox = 20
        zeroy = Graph.MAX_HEIGHT

        # Display axes
        self.create_line(zerox, zeroy, Graph.MAX_WIDTH, zeroy, arrow="last")
        self.create_line(zerox, zeroy, zerox, zeroy - self.ymax * self.coeffy, arrow="last")

        # Display dots
        for name, x, y in self.values:
            x, y = self.coeffx * x + zerox, zeroy - self.coeffy * y
            self.create_oval(x - diametre/2, y - diametre/2, x + diametre / 2, y + diametre / 2, fill="black")

        # Display graduation on x axis
        for ind, name in enumerate(self.permutation):
            x = self.coeffx * (ind + 1) + zerox
            self.create_line(x, zeroy - 5, x, zeroy + 5)
            self.create_text(x, zeroy + 15, text=name)

        # Display Lines between dots
        for i in range(1, len(self.values)):
            x0, y0 = self.coeffx * self.values[i-1][1] + zerox, zeroy - self.coeffy * self.values[i-1][2]
            x1, y1 = self.coeffx * self.values[i][1] + zerox, zeroy - self.coeffy * self.values[i][2]
            self.create_line(x0, y0, x1, y1, width=diametre/3)

