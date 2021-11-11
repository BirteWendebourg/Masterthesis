""" data class to handle and structure the experimental data """
import pandas as pd
from pandastable import Table
# imports for unit handling
import unit_converter as unit_con

class BaseData:
    """ the data base for all future analysis """
    def __init__(self, selected_header, units, data):
        """ initialise the class and fill the values into the variables that were preprocessed by the connection class
        :param units: list of units
        :param header: list of headers
        :param data: pd.DataFrame with raw input data
        """

        # test if all headers and units are there and valid
        'TO DO: header and units as lists or better as a dictionary?'
        self.check_loading = 0
        self.headers = self.check_header(selected_header, len(data.columns)) # list with header names
        if self.check_loading != 0:
            return
        self.units, self.check_loading = unit_con.check_units(units, len(data.columns)) # list with units
        if self.check_loading != 0:
            return

        # create the new dataframe with changed headers and units
        new_units = pd.DataFrame(columns=self.headers, data=[self.units])
        data.columns = self.headers

        # """data variables""" #
        self.datatable = pd.concat([new_units, data])  # dataframe for the processed input data

        'TO DO: initialise default data save path by using the directory of the input file'
        self.data_path = str()  # pathway where the dataset is saved

####################################################################################################
    # """general functions""" #

    # function for saving data
    #   -> how to best connect this to the GUI? Connection class?
    #           check if data set is new or reload and ask for units if it is new
    #           handle save and turn it into save as
    # link function to use unit converter

    def check_header(self, headers, number_of_columns):
        """check if all headers are given"""
        'TO DO: check that every header is unique'
        if len(headers) != number_of_columns:
            self.check_loading = 1
            return None
        for header in headers:
            if header == '':
                self.check_loading = 1
                return None
        return headers

