# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
sys.path.append(getcwd())

from random import randint


def func(x):
    return 2*x


class Interactive(Frame):
    """
    Lower Frame, with the interactive display, showing results for each file
    """

    def __init__(self, parent, filenames, candidates, results):
        """
        Needs a list of file names, a list of candidates (ordered by an algorithm), and a list of results (for each candidate)
        """
        Frame.__init__(self, parent)
        self.left_image = None
        self.right_image = None
        self.left_arrow = self.make_left_arrow(False)
        self.right_arrow = self.make_right_arrow(True)
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
        pass

    def display_next_result(self, event):
        print event.widget.find_closest(event.x, event.y)

    def display_current_graph(self):
        self.graph = Graph(0, 10, 1, func)
        self.graph.afficher(10)

    def pack_elements(self):
        self.left_arrow.pack(side=LEFT)
        self.graph.pack()
        self.right_arrow.pack(side=RIGHT)


class Graph(Canvas):
    MAX_WIDTH = 800  # taille maxi choisi pour mon écran
    MAX_HEIGHT = 200  # idem

    def __init__(self, xmin, xmax, inc, function):
        Canvas.__init__(self, width=Graph.MAX_WIDTH+20, height=Graph.MAX_HEIGHT+20)
        self.xmin = xmin
        self.xmax = xmax

        self.ymin = self.ymax = function(xmin)

        self.values = []

        t = xmin
        while t <= xmax:
            y = function(t)
            if y > self.ymax:
                self.ymax = y
            elif y < self.ymin:
                self.ymin = y
            self.values.append((t, y))
            t += inc

        self.coeffx = (Graph.MAX_WIDTH - 20) / (xmax - xmin)
        self.coeffy = (Graph.MAX_HEIGHT-20) / (self.ymax - self.ymin)

    def afficher(self, diametre):
        zerox = 20
        zeroy = Graph.MAX_HEIGHT

        # Display axes
        self.create_line(zerox, zeroy, Graph.MAX_WIDTH, zeroy, arrow="last")
        self.create_line(zerox, zeroy, zerox, zeroy - self.ymax * self.coeffy, arrow="last")

        # Display dots
        for x, y in self.values:
            x, y = self.coeffx * x + zerox, zeroy - self.coeffy * y
            self.create_oval(x - diametre/2, y - diametre/2, x + diametre / 2, y + diametre / 2, fill="black")
            self.create_line(x, zeroy - 5, x, zeroy + 5)
            self.create_text(x, zeroy + 15, text="Nom du candidat")

        # Display Lines between dots
        for i in range(1, len(self.values)):
            x0, y0 = self.coeffx * self.values[i-1][0] + zerox, zeroy - self.coeffy * self.values[i-1][1]
            x1, y1 = self.coeffx * self.values[i][0] + zerox, zeroy - self.coeffy * self.values[i][1]
            self.create_line(x0, y0, x1, y1, width=diametre/3)

