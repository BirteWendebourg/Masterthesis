""" creates and organises a menu bar with different tabs for input data, analysis and overview """
# imports for the gui
import tkinter as tk


class Menubar(tk.Menu):
    """ menu bar class """
    def __init__(self, parent):
        self.parent = parent
        tk.Menu.__init__(self, self.parent)
        self.drop_menu = tk.Menu(self, tearoff=0)

    def add_to_menu(self, name, option_dict):
        menu = tk.Menu(self.drop_menu, tearoff=0)
        self.add_cascade(label=name, menu=menu)
        for x in option_dict:
            menu.add_command(label=x, command=option_dict[x])
