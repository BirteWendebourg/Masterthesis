""" create a tab for each step of the analysis"""
import tkinter as tk
from tkinter import ttk


'TO DO: change in to a more general class and use multiple times'
class Tabs(ttk.Notebook):
    """ creates tabs for the different parts of the program """
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.tab_control = ttk.Notebook(parent)
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

        # buttons in the different tabs
        self.init_load = tk.Button(master=self.data_tab, text='load new data', command=parent.conD.load)
        self.init_load.pack(side=tk.TOP, expand=tk.YES)
        self.reload = tk.Button(master=self.data_tab, text='load processed data', command=parent.conD.reload)
        self.reload.pack(side=tk.TOP, expand=tk.YES)

        self.new_analyse = tk.Button(master=self.analyse_tab, text='start a new analysis',
                                     command=parent.conA.new_analyse)
        self.new_analyse.pack(side=tk.LEFT, expand=tk.YES)

        tk.Label(self.overview_tab, text='Please perform analyses to see an overview over the results.')\
            .pack(side='top')
