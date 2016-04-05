# -*- coding: utf-8 -*-
from Tkinter import *
from Data.axesPAndroide import *


class FilesMenu(Frame):
    """
    Adds all widgets to select files to test
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.list_files = []
        self.add_files()

    def add_files(self):
        label = Label(self, text="Choose files:", font=("", 16))
        label.grid()
        for f in listFiles:
            checkbtn = Checkbutton(self, text=f, command=lambda: self.add_file(f), padx=10)
            checkbtn.grid()

    def add_file(self, filename):
        print "called"
        if filename in self.list_files:
            self.list_files.remove(filename)
            print self.list_files
        else:
            self.list_files.append(filename)
            print self.list_files
