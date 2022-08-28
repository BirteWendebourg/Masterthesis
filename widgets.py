""" helping functions for the gui design """
import tkinter as tk
from tkinter import ttk
import numpy as np

# global variables
current_function = str()    # variable to store the function formula to be analysed

def function_run1(x_value, a):
    return eval(current_function)

def function_run2(x_value, a, b):
    return eval(current_function)

def function_run3(x_value, a, b, c):
    return eval(current_function)

def function_run4(x_value, a, b, c, d):
    return eval(current_function)

def function_run5(x_value, a, b, c, d, e):
    return eval(current_function)


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


def create_box(window, input):
    """creates a combobox with the unit options next to the header entry fields"""
    box_input = tk.StringVar()
    new_box = ttk.Combobox(window, textvariable=box_input)
    new_box['values'] = input
    new_box['state'] = 'readonly'
    new_box.pack(ipady=4, side='top')
    return box_input
