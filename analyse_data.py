""" analyse class to do the analysis of the experimental data """
import re
import sys
import pandas as pd


class Analyse:
    def __init__(self, starting_parameters, analysis):
        'TO DO: what type of analysis should be done? with which part of the data?'

        self.start = starting_parameters  # list with the starting parameters for the analysis
        self.type = analysis  # name of the analysis that should be performed
        self.rate = None    # column number for the rate that is being investigated
        self.factor = None  # column number for the environmental factor that is being investigated

        self.result = None  # list with end values for the analysis parameters
        self.rmse = None  # rmse of the analysis
        return
