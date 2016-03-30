# -*- coding: utf-8 -*-
from Tkinter import *
import sys
from os import getcwd
sys.path.append(getcwd())

from ui.upper_frame.algo_menu import AlgoMenu
from ui.upper_frame.files_menu import FilesMenu


class UpperFrame(Frame):
    """
    Upper frame of the window
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.left_frame = AlgoMenu(self)
        self.right_frame = FilesMenu(self)
        self.pack_elements()

    def pack_elements(self):
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=RIGHT)

