""" GUI set up. Base of everything else """
# imports for the gui
import tkinter as tk
# imports for the data handling
from pandastable import Table
# own imports
import menu as mb
import tabs as t
from connect_data import ConData as DataConnection
from unit_converter import ConUnit as ConverterConnection
from connect_analyse import ConAnalyse as AnalyseConnection


class Gui(tk.Tk):
    """ This is the base for the program """
    def __init__(self):
        """ initialise the Gui """
        tk.Tk.__init__(self)
        self.title("CuFiP")
        self.geometry("1250x1000")
        self.workaround = 1250    # this is a number needed for a workaround for
        # a pandastable problem that causes the table to not be shown correctly sometimes

        # initialise the connection classes
        self.con_d = DataConnection(self)    # connection to the input data
        self.con_u = ConverterConnection()   # connection to the unit converter
        self.con_a = AnalyseConnection(self.con_d, self)     # connection to the analyses

        # tabs with frames for input, analysis and overview
        'TO DO: maybe move the tabs into the gui to avoid a single use class'
        self.tabs = t.Tabs(self)

        # initialise the menu bar
        self.menu_bar = mb.Menubar(self)
        # file menu
        # creates a dictionary that links the file menu options to its functions
        handle_file = {
            "Load New Data": self.con_d.load,
            "Load Saved Data": self.con_d.reload,
            "Save": self.con_d.save,
            "Save as": self.con_d.save_as,
            "Exit": self.exit
        }
        self.menu_bar.add_to_menu("File", handle_file)
        # data menu
        # creates a dictionary that links the data menu options to its functions
        handle_data = {
            "Convert Unit": self.con_u.converter
        }
        self.menu_bar.add_to_menu("Unit Handling", handle_data)
        # analyse_menu
        # creates lists for the commands and the button names
        # and retrieves them from the analyse classes
   #     analyses_type_commands = list()
   #     analyses_type_button_names = list()
   #     for counter in range(len(self.con_a.ana.kinds)):
            # due to the dynamic nature of available analyse types it is necessary to use a
            # function to wrap the command lambda function
            # (further explanation see wrap_function definition)
   #         analyses_type_commands.append(self.tabs.wrap_function(counter))
   #         analyses_type_button_names.append(self.con_a.ana.kinds[counter] + ' curve analysis')
        # creates a dictionary that links the analyse menu options to its functions
   #     handle_analyses = {}
   #     for name, command in zip(analyses_type_button_names, analyses_type_commands):
   #         handle_analyses[name] = command
   #     self.menu_bar.add_to_menu("Analysis", handle_analyses)

        'TO DO: how different is the Overview data save compared to the raw data save?' \
        'does it need an own option?'
        # overview menu
        # creates a dictionary that links the overview menu options to its functions
        handle_results = {
            "Save results": self.con_a.save,
            "Save plot": self.tabs.save_graph
        }
        self.menu_bar.add_to_menu("Results", handle_results)
        # create the menu bar
        self.config(menu=self.menu_bar)

        'TO DO: analyse_menu: save specific analysis'
        'TO DO: overview_menu: save summary, open specific analysis'

###################################################################################################
# """general functions""" #
    def exit(self):
        """function to close the program"""
        'TO DO: option to stop the closing process'
        self.con_d.save_as()
        self.destroy()

    # """data functions""" #
    def show(self, where, table):
        """show table in where"""
        tab_fra = tk.Frame(self)
        tab_fra.pack(fill=tk.BOTH)
        table = Table(where, dataframe=table, showtoolbar=True, showstatusbar=True)
        table.show()
        # this is a work around for a pandastable problem!
        # the table was sometimes not shown correctly, this is fixed by resizing the window
        size = str(self.workaround) + "x1000"
        self.workaround = self.workaround + 1
        self.geometry(size)
