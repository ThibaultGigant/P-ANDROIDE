# -*- coding: utf-8 -*-
from Tkinter import *
from Data.axesPAndroide import *


class FilesMenu(LabelFrame):
    """
    Adds all widgets to select files to test
    """

    def __init__(self, master):
        LabelFrame.__init__(self, master, text="Choose files")
        self.parent = master
        self.list_files = []
        self.check_buttons = []
        self.add_files()

    def add_files(self):
        label = Label(self, text="Choose files:", font=("", 16))
        label.grid()
        # for f in range(len(listFiles)):
        #     checkbtn = Checkbutton(self, text=listFiles[f], command=lambda name=f: self.add_file(listFiles[name]),
        #                            padx=10)
        #     checkbtn.grid(row=(f % (len(listFiles) / 2)), column=(f / (len(listFiles) / 2)))
        for f in range(len(listFiles)):
            checkbtn = Checkbutton(self, text=listFiles[f], command=lambda name=f: self.add_file(listFiles[name]),
                                   padx=10)
            checkbtn.grid(row=(f % ((len(listFiles) + len(listFrenchFiles)) / 2)),
                          column=(f / ((len(listFiles) + len(listFrenchFiles)) / 2)))
        for f in range(len(listFrenchFiles)):
            checkbtn = Checkbutton(self, text=listFrenchFiles[f],
                                   command=lambda name=f: self.add_file(listFrenchFiles[name]), padx=10)
            checkbtn.grid(row=((f + len(listFiles)) % ((len(listFiles) + len(listFrenchFiles)) / 2)),
                          column=((f + len(listFiles)) / ((len(listFiles) + len(listFrenchFiles)) / 2)))

    def add_file(self, filename):
        """
        :param filename:
        :return:
        """
        if filename in self.list_files:
            self.list_files.remove(filename)
        else:
            self.list_files.append(filename)
