# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
sys.path.append(getcwd())

import matplotlib
matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


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

    def pack_elements(self):
        self.left_arrow.pack(side=LEFT)
        self.right_arrow.pack(side=RIGHT)
