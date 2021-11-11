
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from pandastable import Table
import sys
import widgets as w


class Gui(tk.Tk):
    def __init__(self):
        """window frame"""
        tk.Tk.__init__(self)
        self.title("Curve Fitter")
        self.frame = tk.Frame()
        self.frame.pack()

        """menu bar"""
        self.menu_bar = tk.Menu()
        # file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load Data", command=self.input)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save as", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.save_as)
        # in progress: next menu point...
        # create menu bar
        self.config(menu=self.menu_bar)

        """tabs"""
        # define different windows/tabs in the program
        self.tab_control = ttk.Notebook(self)
        # data tab to manage the input data set
        self.data_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.data_tab, text='Data')
        # analysis tab to run and review the last results
        self.analyse_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.analyse_tab, text='Analysis')
        # overview tab with summary of all analyse runs
        self.overview_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.tab_control.pack(expand=1, fill="both")

        """data variables"""
        self.input_data = pd.DataFrame()    # dataframe for the input data
        self.datatable = pd.DataFrame()     # dataframe for the processed input data
        self.n = 0                          # number of columns in the dataframe
        self.header_entry = []              # entries for the new header names
        self.chosen_units = []              # combobox for choosing the units
        self.data_path = str()              # pathway where the dataset is saved
        self.load_data = None               # initialize window for additional input information

        """analysis variables""" # not implemented yet
        self.button = tk.Button(master=self.analyse_tab, text='press', command=self.action)
        self.button.pack()
        self.variable = tk.Entry(master=self.analyse_tab)
        self.variable.pack()
        self.output = tk.Text(master=self.analyse_tab)
        self.output.pack()

        """overview variables"""

########################################################################################################################
    """data functions"""

    def show(self, table):
        """show table in the data tab"""
        f = tk.Frame(self)
        f.pack(fill=tk.BOTH)
        table = Table(self.data_tab, dataframe=table, showtoolbar=True, showstatusbar=True)
        table.show()
        return 0

    def check_units(self):
        """collect the units and check if all columns got a units"""
        units = []
        missing = False
        for unit in self.chosen_units:
            units.append(unit.get())
            if unit.get() == '':
                missing = True
                break
        # interrupt the loading if there are units missing
        if missing is True:
            unit_error = tk.Toplevel()
            unit_error.title("Unit Error")
            unit_error.geometry('170x100')
            tk.Message(unit_error, text="Please select a unit for all columns!").pack()
            unit_error_close = tk.Button(unit_error, text="Ok", command=unit_error.destroy)
            unit_error_close.pack()
            return False
        else:
            return units

    def check_head(self):
        """collect the headers"""
        new_header = []
        for entry in self.header_entry:
            new_header.append(entry.get())
        return new_header

    def load(self):
        """process additional user input"""
        units = self.check_units()
        if units is False:
            return 1
        else:
            header = self.check_head()

            # create the new dataframe with changed headers and units
            new_units = pd.DataFrame(columns=header, data=[units])
            self.input_data.columns = header
            self.datatable = pd.concat([new_units, self.input_data])

            # show the data in the data tab
            self.show(self.datatable)

            # close the window with the information for the input data
            self.load_data.destroy()
            return 0

    def open_data(self):
        """open the input file"""
        # asks the user for the input file
        filepath = filedialog.askopenfilename()
        if len(filepath) == 0:
            return 0
        else:
            # attempt to open the file
            try:
                stream = open(filepath)
            except IOError:
                sys.stderr.write('{}: cannot open file {}\n'.format(sys.argv[0], filepath))
                exit(1)

            # stop if input file is not a csv-file
            if filepath[len(filepath)-4:] != ".csv":
                file_error = tk.Toplevel()
                file_error.title("File Error")
                file_error.geometry('170x100')
                tk.Message(file_error, text="The loaded file is not compatible!\nPlease use a csv-file.").pack()
                file_error_close = tk.Button(file_error, text="Ok", command=file_error.destroy)
                file_error_close.pack()
                return 1
            else:
                # create a dataframe from the input data
                self.input_data = pd.read_csv(stream)
                # close the input file!
                stream.close()
                return 0

    def info_window(self):
        """get additional information on the input data"""
        # create the loading window
        self.load_data = tk.Toplevel()
        self.load_data.title("Load Data")

        # create the command button to confirm and load the input information
        load_button = tk.Button(self.load_data, text="Load", command=self.load)
        load_button.pack(side='bottom')

        # create frames to structure additional input information
        header_frame = tk.Frame(self.load_data)
        header_frame.pack(side='left')
        unit_frame = tk.Frame(self.load_data)
        unit_frame.pack(side='left')
        tk.Label(header_frame, text='Rename columns').pack(side='top')
        tk.Label(unit_frame, text='Specify unit').pack(side='top')

        # create entries for the option to rename headers
        self.n = len(self.input_data.columns)
        self.header_entry = [w.create_entry(self.input_data.columns[x], header_frame) for x in range(self.n)]
        # create drop down menus for a selection of units
        self.chosen_units = [w.create_box(unit_frame) for _ in range(self.n)]
        return 0

    def input(self):
        """handles all the input data"""
        loaded = self.open_data()
        if loaded == 0:
            # if data could be loaded shows the data
            self.show(self.input_data)
            # open a window for additional information on the input data
            # this is also where the command to complete the loading is initialised
            self.info_window()



####################### under construction #############################################################################

    def exe_save(self, path):
        try:
            with open(self.data_path, "w") as file:
                
                self.datatable.to_csv(file)
                self.data_path = path
                return "saved"
        except FileNotFoundError:
            print("not found")
            return "cancelled"

    def save_as(self):
        path = filedialog.asksaveasfile(filetypes=[("Comma Separated values", "*.csv")])
        self.exe_save(path)
        return 0

    def save(self):
        if self.data_path is None:
            self.save_as()
            return 0
        else:
            self.exe_save(self.data_path)

       # self.save_data = tk.Toplevel()
       # self.save_data.title("Save Data")

 #       load_button = tk.Button(self.save_data, text="Save", command=self.exe_save)
  #      load_button.pack(side='bottom')

   #     tk.Label(self.save_data, text='Filepath:').pack(side='top')

    #    self.header_entry = self.create_entry(self, self.path, self.save_data)

        return 0

    def action(self):
        self.output.insert(tk.END, self.variable.get())
        return 0
