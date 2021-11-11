""" GUI set up. Base of everything else """
# imports for the gui
import tkinter as tk
# imports for the data handling
from pandastable import Table
# own imports
import menu as mb
import tabs as t
from connect_data import ConData as DataConnection
from connect_data import ConUnit as ConverterConnection
from connect_data import ConAnalyse as AnalyseConnection


class Gui(tk.Tk):
    """ This is the base for the program """
    def __init__(self):
        """ initialise the Gui """
        tk.Tk.__init__(self)
        self.title("Curve Fitter")
        self.geometry("1000x500")
        self.workaround = 1000    # this is a number needed for a workaround for
        # a pandastable problem that causes the table to not be shown correctly sometimes

        # initialise the connection classes
        self.conD = DataConnection(self)    # connection to the input data
        self.conU = ConverterConnection()   # connection to the unit converter
        self.conA = AnalyseConnection()     # connection to the analyses

        # initialise the menu bar
        self.menu_bar = mb.Menubar(self)
        # file menu
        handle_file = {         # creates a dictionary that links the file menu options to its functions
            "Load New Data": self.conD.load,
            "Load Saved Data": self.conD.reload,
            "Save": self.conD.save,
            "Save as": self.conD.save_as,
            "Exit": self.exit
        }
        self.menu_bar.add_to_menu("File", handle_file)
        # data menu
        handle_data = {         # creates a dictionary that links the data menu options to its functions
            "Convert Unit": self.conU.converter
        }
        self.menu_bar.add_to_menu("Unit Handling", handle_data)
        # analyse_menu
        handle_analyses = {  # creates a dictionary that links the analyse menu options to its functions
            "Start new analyse": self.conA.new_analyse
        }
        self.menu_bar.add_to_menu("Analysis", handle_analyses)

        'TO DO: how different is the Overview data save compared to the raw data save? does it need an own option?'
        # overview menu
        handle_results = {  # creates a dictionary that links the analyse menu options to its functions
            "Save overview results": self.conD.save,
            "Save overview results as": self.conD.save_as,
        }
        self.menu_bar.add_to_menu("Results", handle_results)
        # create the menu bar
        self.config(menu=self.menu_bar)

        'TO DO: analyse_menu: new analysis (maybe different analysis type options' \
            'like temp, light or nutrient dependent), save specific analysis'
        'TO DO: overview_menu: save summary, open specific analysis'

        # tabs with frames for input, analysis and overview
        'TO DO: maybe move the tabs into the gui to avoid a single use class'
        self.tabs = t.Tabs(self)

####################################################################################################
# """general functions""" #

    def exit(self):
        """function to close the program"""
        'TO DO: option to stop the closing process'
        self.conD.save_as()
        self.destroy()
        return

    # """data functions""" #
    def show(self, where, table):
        """show table in where"""
        tab_fra = tk.Frame(self)
        tab_fra.pack(fill=tk.BOTH)
        table = Table(where, dataframe=table, showtoolbar=True, showstatusbar=True)
        table.show()
        # this is a work around for a pandastable problem!
        # the table was sometimes not shown correctly, this is fixed by resizing the window
        size = str(self.workaround) + "x500"
        self.workaround = self.workaround + 1
        self.geometry(size)
        return 0
