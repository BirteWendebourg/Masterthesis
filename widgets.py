""" helping functions for the gui design """
import tkinter as tk
from tkinter import ttk


def data_window():
    """get additional information on the input data"""
    # create the loading window
    load_data = tk.Toplevel()
    load_data.title("Load Data")
    return 0


def create_entry(name, window):
    """creates a new entry field with the default input name in it"""
    # """which appears in the specified window""" #
    entry_input = tk.StringVar()
    new_entry = tk.Entry(window, textvariable=entry_input)
    new_entry.pack(ipady=3)
    new_entry.insert(0, name)
    return entry_input


def create_box(window):
    """creates a combobox with the unit options next to the header entry fields"""
    box_input = tk.StringVar()
    new_box = ttk.Combobox(window, textvariable=box_input)
    new_box['values'] = ('without unit', '°C', '°F', 'K', '/day', '/hour', 'ml', u'\u03bc'+'l',
                         'g', 'mg', u'\u03bc'+'g', 'pg', 'cells/ml', 'cells/'u'\u03bc'+'l',
                         'cells/'u'\u03bc'+'g', 'cells/pg', 'cells/mol', 'cells/'u'\u03bc'+'mol',
                         u'\u03bc'+'mol O2/cell', u'\u03bc'+'mol C/cell', u'\u03bc'+'mol O2/ml',
                         'mol O2/ml', u'\u03bc'+'mol O2/'u'\u03bc'+'l', 'mol O2/'u'\u03bc'+'l',
                         u'\u03bc'+'mol C/ml', 'mol C/ml', u'\u03bc'+'mol C/'u'\u03bc'+'l',
                         'mol C/'u'\u03bc'+'l', u'\u03bc'+'mol O2/cell day', 'mol O2/cell day',
                         u'\u03bc'+'mol O2/cell hour', 'mol O2/cell hour',
                         u'\u03bc'+'mol C/cell day', 'mol C/cell day', u'\u03bc'+'mol C/cell hour',
                         'mol C/cell hour', u'\u03bc'+'mol C/'u'\u03bc'+'mol O2', 'mol C/mol O2',
                         'nmol O2/cell', 'nmol C/cell', 'nmol O2/ml', 'nmol O2/'u'\u03bc'+'l',
                         'nmol C/ml', 'nmol C/'u'\u03bc'+'l', 'nmol O2/cell day',
                         'nmol O2/cell hour', 'nmol C/cell day', 'nmol C/cell hour',
                         'nmol C/nmol O2')
    new_box.pack(ipady=4)
    return box_input
