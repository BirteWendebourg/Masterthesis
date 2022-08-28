""" helper class that connects the GUI to the data class """
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
        self.filepath = str()       # string to save the path to the data
        self.first_save = True
        # boolean to make sure that the input file is only overwritten when the user wants this!
        self.new_data = True
        # boolean to make sure that the current date is only overwritten when the user wants this!
        self.load_data = None       # initialize window for additional input information
        self.header_entry = []      # entries for the new header names
        self.chosen_units = []    # combobox for choosing the units

    # visuals and windows for data input
    def open_file(self):
        """open the input file and check if it is opened successfully"""
        # asks the user for the input file
        self.filepath = filedialog.askopenfilename(
            filetypes=[('Comma Separated Values', '*.csv')])
        if len(self.filepath) == 0:
            return 1
        # attempt to open the file
        with open(self.filepath) as stream:
            # create a dataframe from the input data
            self.input_data = pd.read_csv(stream, engine='python', sep=None, na_values="NaN")
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
            self.gui.tabs.set_up_data_tab(1)
        return 0

    def process_info_window(self):
        """process additional user input"""
        # collect the new headers
        header = [entry.get() for entry in self.header_entry]

        # checks if all units are correctly selected
        units = [unit.get() for unit in self.chosen_units]

        # initialization of the data class object
        # during the initialization the headers and units are checked
        self.data = base.BaseData(header, units, self.input_data)
        # when headers are missing
        if self.data.check_loading == 1:
            header_error = tk.Toplevel()
            header_error.title("Header Error")
            header_error.geometry('200x100')
            tk.Message(header_error, text="Please select a header for all columns!")\
                .pack(side='top')
            'TODO: add which header needs to be set/that Unnamed or something similar' \
                'that is easier to spot, is not a valid header name'
            header_error_close = tk.Button(header_error, text="Ok", command=header_error.destroy)
            header_error_close.pack()
            return 1
        # when units are missing or not valid
        if self.data.check_loading == 2:
            unit_error = tk.Toplevel()
            unit_error.title("Unit Error")
            unit_error.geometry('200x100')
            tk.Message(unit_error, text="Please select a unit for all columns!").pack(side='top')
            unit_error_close = tk.Button(unit_error, text="Ok", command=unit_error.destroy)
            unit_error_close.pack()
            return 1
        # only happens if both if statements are not true!
        # show the data in the data tab
        self.gui.show(self.gui.tabs.data_tab, self.data.datatable)
        # close the window with the information for the input data
        self.load_data.destroy()
        # reset and load the analyse tab
        self.gui.con_a.wrap_frame = None
        self.gui.tabs.set_up_analyse_tab()
        self.new_data = False
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
        'TODO: move units to unit converter class'
        units = ('without unit', '°C', '°F', 'K',           # temperature
                 'PAR', u'\u03bc'+ 'mol photons/m**2 s',    # light
                 '/day', '/hour', 'ml', u'\u03bc' + 'l',    # time and volume
                 'g', 'mg', u'\u03bc' + 'g', 'pg',          # weight
                 'g/mol', 'mg/mol', u'\u03bc' + 'g/mol',    # mass
                 'pg/mol',
                 'km', 'm', 'cm', 'mm', u'\u03bc' + 'm',    # distance/size
                 'cells/ml', 'cells/'u'\u03bc' + 'l',       # cells per volume
                 'cells/'u'\u03bc' + 'g', 'cells/pg',       # cells per weight
                 'cells/mol', 'cells/'u'\u03bc' + 'mol',    # cells per mol
                 u'\u03bc' + 'mol O2/cell', u'\u03bc' + 'mol C/cell',   # O2 and C per cell
                 u'\u03bc' + 'mol O2/ml', 'mol O2/ml', u'\u03bc' + 'mol O2/'u'\u03bc' + 'l',
                 'mol O2/'u'\u03bc' + 'l',                  # O2 per volume
                 u'\u03bc' + 'mol C/ml', 'mol C/ml', u'\u03bc' + 'mol C/'u'\u03bc' + 'l',
                 'mol C/'u'\u03bc' + 'l',                   # C per volume
                 u'\u03bc' + 'mol O2/cell day', 'mol O2/cell day', u'\u03bc' + 'mol O2/cell hour',
                 'mol O2/cell hour',                        # O2 per time
                 u'\u03bc' + 'mol C/cell day', 'mol C/cell day', u'\u03bc' + 'mol C/cell hour',
                 'mol C/cell hour',                         # C per time
                 u'\u03bc' + 'mol C/'u'\u03bc' + 'mol O2', 'mol C/mol O2',
                 'nmol C/nmol O2',                          # C per O2
                 'nmol O2/cell', 'nmol C/cell',             # O2 and C per cell
                 'nmol O2/ml', 'nmol O2/'u'\u03bc' + 'l', 'nmol C/ml',
                 'nmol C/'u'\u03bc' + 'l',                  # O2 and C per volume
                 'nmol O2/cell day', 'nmol O2/cell hour', 'nmol C/cell day',
                 'nmol C/cell hour')                        # O2 and C per cell per time
        self.chosen_units = [w.create_box(unit_frame, units) for _ in range(col_num)]
        return 0

    # loading data
    def load(self):
        """loads new data"""
        # warn the user when there is already data loaded
        if self.new_data is False:
            self.check_current_state(0)
            return
        self.present_unprocessed()
        self.info_window()
        return

    def reload(self):
        """loads already processed data"""
        # warn the user when there is already data loaded
        if self.new_data is False:
            self.check_current_state(1)
            return
        self.present_unprocessed()
        header = []
        for column in self.input_data.columns:
            header.append(column)
        data = self.input_data.iloc[1:]
        data = data.astype("float64", errors='ignore')
        print(data.info())

        self.data = base.BaseData(header, self.input_data.iloc[0], data)
        if self.data.check_loading == 0:
            self.gui.tabs.set_up_analyse_tab()
            return
        del self.data
        self.info_window()
        'TODO: check if headers and units are correct'
        'TODO: if headers and/or units are not correct,'
        'TODO: not working correctly check why units cannot be set with this method'
        'open a window to allow the user to make changes'

    # saving data
    def save(self):
        """save processed input data with correct headers and units
         at the original or already defined location"""
        if self.first_save is True:
            self.save_as()
            return 0
        with open(self.filepath, mode='w') as stream:
            self.data.datatable.to_csv(stream, index=False)
        return 0

    def save_as(self):
        """save processed input data with correct headers and units at the chosen location"""
        save_path = filedialog.asksaveasfilename(filetypes=[('Comma Separated Values', '*.csv')])
        if len(save_path) == 0:
            return 1
        self.filepath = save_path
        self.first_save = False
        with open(self.filepath, mode='w') as stream:
            self.data.datatable.to_csv(stream, index=False)
        return 0

    # handeling old data, when new data is loaded
    def check_current_state(self, loading):
        """ handles already loaded data """
        data_warning = tk.Toplevel()
        data_warning.title("Data Warning")
        data_warning.geometry('300x125')
        tk.Label(data_warning, text="\nDo you want to load new data?\n"
                                      "The current data and analyses will "
                                      "be deleted in the process!",
                 wraplength=250, justify=tk.CENTER).pack(side='top')
        tk.Button(data_warning, text="Cancel", command=lambda: [data_warning.destroy()])\
            .pack(side=tk.LEFT)
        tk.Button(data_warning, text="Save & Continue", command=lambda:
        [data_warning.destroy(), self.go_on(1, loading)]).pack(side=tk.LEFT)
        tk.Button(data_warning, text="Continue", command=lambda:
        [data_warning.destroy(), self.go_on(0, loading)]).pack(side=tk.LEFT)

    def go_on(self, saving, going):
        if saving == 1:
            self.save()
        self.new_data = True
        if going == 0:
            self.load()
        else:
            self.reload()
