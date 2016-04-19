# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
sys.path.append(getcwd())

from ui.top_menu import TopMenu
from ui.upper_frame.upper_frame import UpperFrame


class MainWindow(Frame):
    """
    Frame containing all other ui elements
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.mode = "benchmark"
        # self.top_menu = TopMenu(self)
        self.upper_frame = UpperFrame(self)
        # self.upper_frame = None
        self.lower_frame = None
        self.pack_elements()
        Label(self, text="Test").pack()

    def pack_upper_frame(self):
        if self.upper_frame:
            self.upper_frame.pack(side=TOP)

    def pack_lower_frame(self):
        if self.lower_frame:
            self.lower_frame.pack(side=BOTTOM)

    def pack_elements(self):
        self.pack_upper_frame()
        self.pack_lower_frame()

    def set_upper_frame(self, frame):
        """
        Change the upper_frame
        :param frame: widget that will replace the old one
        """
        if self.upper_frame:
            self.upper_frame.destroy()
        self.upper_frame = frame
        self.pack_upper_frame()

    def set_lower_frame(self, frame):
        """
        Change the lower_frame
        :param frame: widget that will replace the old one
        """
        if self.lower_frame:
            self.lower_frame.destroy()
        self.lower_frame = frame
        self.pack_lower_frame()

    def set_mode(self, mode):
        self.mode = mode


def launch():
    root = Tk()
    # root.resizable(width=False, height=False)

    main_window = MainWindow(root)
    main_window.pack()

    root.mainloop()


def test():
    fenetre = Tk()

    UpperFrame(fenetre).pack()

    fenetre.mainloop()


if __name__ == '__main__':
    #launch()
    test()
