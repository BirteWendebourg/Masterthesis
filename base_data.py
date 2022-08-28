""" data class to handle and structure the experimental data """
# data handling in python
import pandas as pd
#from pandastable import Table
# imports for unit handling
import unit_converter as unit_con

class BaseData:
    """ the data base for all future analysis """
    def __init__(self, selected_header, units, data):
        """ initialise the class and fill the values into the variables
        that were preprocessed by the connection class
        :param units: list of units
        :param header: list of headers
        :param data: pd.DataFrame with raw input data
        """

        # test if all headers and units are there and valid
        'TO DO: header and units as lists or better as a dictionary?'
        self.check_loading = 0
        # list with header names
        self.headers = self.check_header(selected_header, len(data.columns))
        if self.check_loading != 0:
            return
        # list with units
        self.units, self.check_loading = unit_con.check_units(units, len(data.columns))
        if self.check_loading != 0:
            return

        # create the new dataframe with changed headers and units
        new_units = pd.DataFrame(columns=self.headers, data=[self.units])
        data.columns = self.headers

        # create a list with important structural information of the input data (numerical...?)
        self.data_types = data.dtypes                   # list with information about the data
 #       for column in data.columns:
  #          print(column)
   #         print(type(column))
    #        print(type(data[column][1]))
            #for count in range(len(data[column])):
             #   print(data[column][count], type(data[column][count]))
      #  print(data)
       # print(self.data_types)

        # """data variables""" #
        self.datatable = pd.concat([new_units, data])   # dataframe for the processed input data

##################################################################################################
    # """general functions""" #

    def __del__(self):
        print()

    # function for saving data
    #   -> how to best connect this to the GUI? Connection class?
    #           check if data set is new or reload and ask for units if it is new
    #           handle save and turn it into save as
    # link function to use unit converter

    def check_header(self, headers, number_of_columns):
        """check if all headers are given"""
        'TO DO: check that every header is unique, up til now only looks if the headers are there'
        if len(headers) != number_of_columns:
            self.check_loading = 1
            return None
        for header in headers:
            if header == '' or 'Unnamed:' in header:
                'TODO: change Unnamed to nothing or something similar that is easy to spot'
                print("found NaN in header")
                self.check_loading = 1
                return None
        return headers
