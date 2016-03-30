# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import Combobox
from tkFileDialog import *
from tkMessageBox import *

apropos_message = """
P-ANDROIDE Project
"""


class TopMenu(Menu):
    """
    Class creating a Top Menu, on top of the window, or in the menu bar for Mac
    Each method creates a pulldown menu
    """
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.menu_mode()
        self.menu_aide()
        self.parent.parent.config(menu=self)

    def menu_mode(self):
        menu1 = Menu(self, tearoff=0)
        menu1.add_command(label="Benchmark", command=lambda: self.parent.set_mode("benchmark"))
        menu1.add_command(label="Interactive", command=lambda: self.parent.set_mode("interactive"))
        menu1.add_separator()
        menu1.add_command(label="Close", command=self.parent.quit)
        self.add_cascade(label="Mode", menu=menu1)

    def menu_aide(self):
        menu2 = Menu(self, tearoff=0)
        menu2.add_command(label="About", command=self.apropos)
        self.add_cascade(label="About", menu=menu2)

    @staticmethod
    def apropos():
        showinfo("P-ANDROIDE", apropos_message)

