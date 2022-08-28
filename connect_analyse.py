""" helper class that connects the GUI to the analyse class """
# imports for the gui
import tkinter as tk
# imports for the data handling
from tkinter import filedialog
import pandas as pd
# from pandastable import Table
import numpy as np

# matplot imports to show the graphs
import matplotlib
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib import pyplot as plt

# own imports
# import base_data as base
import analyse_data as analyse
import widgets as w

# addition to the matplot import
matplotlib.use('TkAgg')


class ConAnalyse:
    """class that connects the gui to everything analysis related"""
    'TODO: have a look if all instance attributes are necessary as instance attributes'
    def __init__(self, datacon, gui):
        self.con_data = datacon         # connects to the data connection class
        self.gui = gui                  # connection to the gui

        self.ana = analyse.AnalyseData()
        self.known_analyses = []
        for i in range(len(self.ana.kinds)):
            self.known_analyses.append((self.ana.kinds[i], i))

        'TODO: überlegen ob RunAnalyses früher initialisiert' \
            'und diese Varialen direkt festgelegt werden können'
        self.x_values_selection = None
        self.y_values_selection = None
        self.x_values = None
        self.y_values = None

        self.wrap_frame = None          # initialize frame for choosing an analysis type
        self.choice = tk.IntVar()
        # kind of analyses that was chosen as a number careful!
        # needs to be a tk.IntVar() or tk.StringVar()!

        self.function_choice = []       # list of booleans to show which functions where choosen
        self.parameters = []            # list of lists with the starting parameters

        self.run = []                   # list of analyses from one analyse run
        self.figure = None              # variable to store the analyse plot in

    # provide headers for the data and start the analysis
    def process_ana_tab(self, choice_count):
        """process the information given by the user and start the requested analyses
        choice_count gives the amount of analyses to be done"""
        self.run = []
        # reinitialise the variable that saves all the runs information
        # removes all old information of the previous run

        # process the users data choice
        # sorts the datatable in the order of the choosen x value
        sorted_data = self.con_data.data.datatable.iloc[1:].sort_values(self.x_values_selection.get())
        self.x_values = sorted_data[self.x_values_selection.get()]
        self.y_values = sorted_data[self.y_values_selection.get()]

        # get the amount of chosen functions
        count = 0
        para_count = 0

        for function_count in range(len(self.ana.functions)):
            # iterate over all known functions
            if count == choice_count:
                break
            # but only if there are still chosen functions missing
            if self.ana.functions[function_count].kind == self.ana.kinds[self.choice.get()]:
                if self.function_choice[para_count].get() == 1:
                    # check the analyse kind and if the function was chosen
                    start_parameter = []
                    for para in self.parameters[para_count]:
                        # prepares the parameters for the analysis
                        # by doing this here all parameter input for analysis
                        # not chosen by the user will not be processed
                        start_parameter.append(float(para.get()))
                    self.run.append(analyse.AnalyseRun(self.ana.functions[function_count],
                                                       start_parameter, self.x_values,
                                                       self.y_values))
                    # create an AnalyseRun class object
                    self.run[count].run_optimum_analyses()
                    # perform the analyse

                    count += 1
                para_count += 1

        # for func_parameters in self.parameters:
        #     print(func_parameters)
        #     start_para = []
        #     for parameter in func_parameters:
        #         print(parameter.get())
        #         try:
        #             start_para.append(int(parameter.get()))
        #         except ValueError:
        #             int_error = tk.Toplevel()
        #             int_error.title("Start Parameter Error")
        #             int_error.geometry('270x100')
        #             tk.Message(int_error, text="Please give an integer as starting parameter!")\
        #                 .pack()
        #             int_error_close = tk.Button(int_error, text="Ok", command=int_error.destroy)
        #             int_error_close.pack()
        #             return 1
        #     print(start_para)

    # visuals for analysis selection
    def show_choice(self):
        """show the functions available for the selected analysis kind"""
        # structure for the function selection
        for function in self.ana.functions:
            if function.kind == self.ana.kinds[self.choice.get()]:
                frame1 = tk.Frame(self.wrap_frame)
                frame1.pack(fill=tk.X)

                frame2 = tk.Frame(frame1)
                frame2.pack(side=tk.LEFT)

                frame3 = tk.Frame(frame1)
                frame3.pack(side=tk.LEFT)

                frame4 = tk.Frame(self.wrap_frame)
                frame4.pack(fill=tk.X)

                var = tk.IntVar()
                text = function.name
                function_checkbox = tk.Checkbutton(frame2, text=text,
                                                   variable=var, width=20, anchor='w')
                function_checkbox.pack(side=tk.TOP, padx=5, pady=5, anchor='w')
                self.function_choice.append(var)
                tk.Label(frame3, text=function.formula).pack(side=tk.TOP, padx=5, pady=5,
                                                                  anchor ='w')

                func_parameters = []
                tk.Label(frame4, text='Starting parameters:', width=15, padx=20).pack(side=tk.LEFT,
                                                                                      anchor='w')
                for _ in range(function.start):
                    # this has to be a string
                    # otherwise integers with leading zeroes will be interpreted as octal
                    parameter = tk.StringVar()
                    new_entry = tk.Entry(frame4, textvariable=parameter, width=15)
                    new_entry.pack(side=tk.LEFT, pady=5, padx=5)
                    new_entry.insert(0, 0)
                    func_parameters.append(parameter)
                self.parameters.append(func_parameters)
        return 0

    def analyse_set_up(self, initial_choice):
        """get additional information on the input data"""
        self.choice.set(initial_choice)

        if self.wrap_frame is None:
            self.wrap_frame = tk.Frame(self.gui.tabs.analyse_tab)
            self.wrap_frame.pack(fill=tk.X)
        elif len(self.wrap_frame.winfo_children()) != 0:
            # clean the frame for a different kind of analyse run"""
            for widget in self.wrap_frame.winfo_children():
               widget.destroy()

        # reinitialise the lists of the chosen functions and starting parameters
        # for the new chosen kind of analysis
        self.function_choice = []
        self.parameters = []
        self.show_choice()

    # saving results
    def save(self):
        """save example data of the resulting functions and their key figures"""
        # collect and sort all the information that should be saved
        para_name = ('a', 'b', 'c', 'd', 'e')
        result_table = pd.DataFrame()

        'TODO: add option which functions data you want to save'
        result_count = 0
        for result in self.run:
            # build the "header"
            line1 = ('Function: ', result.function.name, 'Formula: ', result.function.formula)
            line2 = ('R-square: ', result.results[4], 'adjusted R-square: ', result.results[5],
                     'RMSE: ', result.results[10])
            line3 = ('SSE: ', result.results[6][0], 'SSR: ', result.results[6][1],
                     'SST: ', result.results[6][2])
            line4 = ('Parameter: ', 'Start-Value', 'Estimated-Value:', 'Variance:', 'Std. Error:',
                     '95% Confidence Interval: ')
            para_lines = []
            for para_count in range(len(result.results[0])):
                para_line = []
                para_line.append(para_name[para_count] + ': ')      # Parameter name
                para_line.append(result.start[para_count])          # start value
                para_line.append(result.results[0][para_count])     # estimated value
                para_line.append(result.results[2][para_count])     # variance
                para_line.append(result.results[3][para_count])     # standard error
                para_line.append(result.results[0][para_count] - result.results[9][para_count])
                                                                    # confidence lower bound
                para_line.append(result.results[0][para_count] + result.results[9][para_count])
                                                                    # confidence upper bound
                para_lines.append(para_line)
            result_count += 1


            # predicted data
            w.current_function = result.function.formula
            data_lines = [[self.x_values_selection.get(), self.y_values_selection.get() +
                           ' original', self.y_values_selection.get() + ' fit', '']]
            for count in range(len(self.con_data.data.datatable[self.x_values_selection.get()])-1):
                data_line = []
                # x values
                data_x = self.con_data.data.datatable[self.x_values_selection.get()]
                data_line.append(data_x.iloc[count+1])
                # original y values
                data_y = self.con_data.data.datatable[self.y_values_selection.get()]
                data_line.append(data_y.iloc[count + 1])
                # fitted y values
                if result.function.start == 1:
                    data_line.append(w.function_run1(data_x.iloc[count+1], result.results[0][0]))
                elif result.function.start == 2:
                    data_line.append(w.function_run2(data_x.iloc[count+1], result.results[0][0],
                                                     result.results[0][1]))
                elif result.function.start == 3:
                    data_line.append(w.function_run3(data_x.iloc[count+1], result.results[0][0],
                                                     result.results[0][1], result.results[0][2]))
                elif result.function.start == 4:
                    data_line.append(w.function_run4(data_x.iloc[count+1], result.results[0][0],
                                                     result.results[0][1], result.results[0][2],
                                                     result.results[0][3]))
                elif result.function.start == 5:
                    data_line.append(w.function_run5(data_x.iloc[count+1], result.results[0][0],
                                                     result.results[0][1], result.results[0][2],
                                                     result.results[0][3], result.results[0][4]))
                data_line.append('')
                data_lines.append(data_line)

            # join all the information into one pandas table
            header_table = pd.DataFrame(data=(line1, line2, line3, line4))
            para_table = pd.DataFrame(data=para_lines)
            data_table = pd.DataFrame(data=data_lines)
            result_table = pd.concat([result_table, header_table, para_table, data_table])

        # get file path and save the table
        result_path = filedialog.asksaveasfilename(filetypes=[('Comma Separated Values', '*.csv')])
        if len(result_path) == 0:
            return 0
        with open(result_path, mode='w') as stream:
            result_table.to_csv(stream, index=False)
        return 0
