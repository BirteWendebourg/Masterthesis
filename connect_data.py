""" helper class that connects the GUI to the data classes """
# imports for the gui
import tkinter as tk
# imports for the data handling
from tkinter import filedialog
import pandas as pd
# from pandastable import Table
# own imports
import base_data as base
import widgets as w


class ConData:
    """class that connects the gui to the data"""
    def __init__(self, gui):
        self.gui = gui     # connection to gui object
        self.data = None   # empty connection to the experimental data object
        # can only be filled once the input data has been processed

        # variables to handle the data input to store it in a base_data class object
        self.input_data = pd.DataFrame()    # dataframe for the input data

        """data handling functions"""
        'TO DO: load data  ->  check if data set is new or reload and ask for units if it is new'
        'TO DO: save and save as  ->   handle save and turn it into save as'
        self.load_data = None       # initialize window for additional input information
        self.header_entry = []      # entries for the new header names
        self.chosen_units = []    # combobox for choosing the units

    # data input
    def open_file(self):
        """open the input file and check if it is opened successfully"""
        # asks the user for the input file
        filepath = filedialog.askopenfilename(filetypes=[('Comma Separated Values', '*.csv')])
        if len(filepath) == 0:
            return 1
        # attempt to open the file
        with open(filepath) as stream:
            # create a dataframe from the input data
            self.input_data = pd.read_csv(stream)
            return 0

    def present_unprocessed(self):
        """checks if new data can be loaded and shows the new unprocessed data"""
        # check if there is data already loaded and needs to be saved
        'TO DO: if there is already data loaded, should it be saved before loading other data'
        #    if self.old_data() != 0:
        #        return 0
        # check that the input file opens correctly
        if self.open_file() == 0:
            # destroy the load buttons to make room and show the new input data
            self.gui.tabs.init_load.destroy()
            self.gui.tabs.reload.destroy()
            self.gui.show(self.gui.tabs.data_tab, self.input_data)
        return 0

    def process_info_window(self):
        """process additional user input"""
        # collect the new headers
        header = [entry.get() for entry in self.header_entry]

        # checks if all units are correctly selected
        units = [unit.get() for unit in self.chosen_units]

        # initialization of the data class object
        # during the initialization the headers and units are checked
        data = base.BaseData(header, units, self.input_data)
        # when headers are missing
        if data.check_loading == 1:
            header_error = tk.Toplevel()
            header_error.title("Header Error")
            header_error.geometry('200x100')
            tk.Message(header_error, text="Please select a header for all columns!").pack(side='top')
            header_error_close = tk.Button(header_error, text="Ok", command=header_error.destroy)
            header_error_close.pack()
            return 1
        # when units are missing or not valid
        elif data.check_loading == 2:
            unit_error = tk.Toplevel()
            unit_error.title("Unit Error")
            unit_error.geometry('200x100')
            tk.Message(unit_error, text="Please select a unit for all columns!").pack(side='top')
            unit_error_close = tk.Button(unit_error, text="Ok", command=unit_error.destroy)
            unit_error_close.pack()
            return 1
        else:
            # show the data in the data tab
            self.gui.show(self.gui.tabs.data_tab, data.datatable)

            # close the window with the information for the input data
            self.load_data.destroy()
            return 0

    def info_window(self):
        """get additional information on the input data"""
        # create the loading window
        self.load_data = tk.Toplevel()
        self.load_data.title("Load Data")

        # create the command button to confirm and load the input information
        'TO DO: check if headers and units are given correctly'
        load_button = tk.Button(self.load_data, text="Load", command=self.process_info_window)
        load_button.pack(side='bottom')

        # create frames to structure additional input information
        header_frame = tk.Frame(self.load_data)
        header_frame.pack(side='left')
        unit_frame = tk.Frame(self.load_data)
        unit_frame.pack(side='left')
        tk.Label(header_frame, text='Rename columns').pack(side='top')
        tk.Label(unit_frame, text='Specify unit').pack(side='top')

        # create entries for the option to rename headers
        col_num = len(self.input_data.columns)
        self.header_entry = [w.create_entry(self.input_data.columns[x], header_frame)
                             for x in range(col_num)]
        # create drop down menus for a selection of units
        self.chosen_units = [w.create_box(unit_frame) for _ in range(col_num)]
        return 0

    def load(self):
        """loads new data"""
        self.present_unprocessed()
        'TO DO: open window to ask for headers and units'
        self.info_window()
        return 0

    def reload(self):
        """loads already processed data"""
        self.present_unprocessed()
        'TO DO: check if headers and units are correct'
        'TO DO: if headers and/or units are not correct,' \
        'open a window to allow the user to make changes'

    def save(self):
        """save processed input data with correct headers and units
         at the original or already defined location"""
        'TO DO: implement saving process'
        return 0

    def save_as(self):
        """save processed input data with correct headers and units at the chosen location"""
        'TO DO: ask user for the location to save the input data and start the saving process'
        self.save()
        return 0

    'TO DO: implement connection to the base data where the data will be stored'











'TO DO: move ConUnit and ConAnalyse into own files'


class ConUnit:
    """connection to the unit converter"""
    def __init__(self):
        return

    def converter(self):
        return












class ConAnalyse:
    def __init__(self):
        return

    def new_analyse(self):
        """starts a new analysis"""
        return

    # starting an analysis
    # preprocessing of the data (splice to only give the analysis the needed data)
    # option to select the data, the analysis type and the starting parameters,
    # provide default starting parameters
    #   -> should this be here or in the GUI?
    # option to call multiple Analysis objects
    # function to show the results (key values, graph...)·
