""" analyse class to do the analysis of the experimental data """
# imports for the data handling
import re
import numpy as np
#import pandas as pd
import pandas as pd
from scipy import optimize
from scipy import stats
#import matplotlib.pyplot as plt

# own imports
#import base_data as data
#import functions as fun
import widgets as w

"""adding a developers option"""
dev_mode = False
# activates the developer mode in which different parameters can be tested and documented easily
# data loading and selection is still the same as in the normal mode
# parameters for the dev_mode
number_of_parameter_option_a = 51  # decide on how many values a should have
step_size_a = -0.28  # decide on the distance between the values of a
number_of_parameter_option_b = 51  # decide on how many values b should have
step_size_b = 22.94  # decide on the distance between the values of b
number_of_parameter_option_c = 1  # decide on how many values c should have
step_size_c = 11.41  # decide on the distance between the values of c
number_of_parameter_option_d = 1  # decide on how many values d should have
step_size_d = 11.41  # decide on the distance between the values of d
number_of_parameter_option_e = 1  # decide on how many values e should have
step_size_e = 1  # decide on the distance between the values of e
'TODO: get it from the gui class'

class Function:
    """class that knows and saves all knowledge the program has about a function"""
    'TODO: either include into Analyse_Data or maybe include the adding and removing options here' \
    'or maybe include the Analysis_Run functions here'
    def __init__(self, identifier, name, kind, formula, start):
        self.identifier = identifier
        self.name = name
        self.kind = kind
        self.formula = formula
        self.start = int(start)

class AnalyseData:
    """class for retrieving the functions and what is known about them out of the file
    'Functions.txt' and feeding them into function classes"""
    def __init__(self):
        known_functions = self.open_file()
        names = re.findall(r'name: \'.*', known_functions)
        kinds = re.findall(r'kind: \'.*', known_functions)
        formulas = re.findall(r'formula: .*', known_functions)
        numberofvariables = re.findall(r'number of starting parameters: \d+', known_functions)
        self.functions = []
        temp_kinds = []
        for counter, name in enumerate(names):
            identifier = counter
            name = name.split(': ')[1][1:-1]
            kind = kinds[counter].split(': ')[1][1:-1]
            temp_kinds.append(kind)
            formula = formulas[counter].split(': ')[1]
            numberofvariable = numberofvariables[counter].split(': ')[1]
            self.functions.append(Function(identifier, name, kind, formula, numberofvariable))
        self.kinds = np.unique(temp_kinds)

    @staticmethod
    def open_file():
        """open the function file to load in the known functions"""
        # attempt to open the file
        'TODO: generalize position of the Function file'
        with open("/home/tiriki/PycharmProjects/Masterthesis/Functions","r") as stream:
            # create a dataframe from the input data
            return stream.read()

class AnalyseRun:
    """class that handles the analysis of a given function with the given parameters and data"""
    def __init__(self, function, starting_parameter, x_value, y_value):
        'TODO: what kind of analysis should be done? with which part of the data?'
        self.x_value = x_value  # regression variable
                                # environmental factors (temperature, nutrients...)
        self.y_value = y_value  # dependent variable
                                # biological factors (growth rate, mortality rate...)
        self.ny_value = None    # variable for the calculated y_values
        self.residuals = None   # variable for the residuals
        self.low_bound = None   # lower prediction bound
        self.up_bound = None    # upper prediction bound

        # list with the function and it's starting parameters for the analysis
        # TODO: figure out how to make this a list of a list of two items,
        #  so that the second empty value isn't needed anymore
        self.start = np.array(starting_parameter, dtype='float64')
        if dev_mode == True:
            self.start_parameter = []

        self.function = function  # function class object of the function that should be performed

        self.results = []   # list with all interesting values to evaluate the fit,
        # in the following order
        # parameters, covariance, variance, std-error, r_squared, adjusted r_squared,
        # list of SSE & SSR & SST, degrees of freedom, critical t-value,
        # upper & lower confidence bounds


    def run_optimum_analyses(self):
        """makes the analysis for optimum analyses"""
        'TODO make more general for all functions and kinds of functions'
        x_value = np.array(self.x_value.values.flatten(), dtype='float64')
        y_value = np.array(self.y_value.values.flatten(), dtype='float64')
        w.current_function = self.function.formula

        if self.function.start == 1:
            if dev_mode is True:
                start = None
                option = 0
                param = []
                cov = []
                while option < number_of_parameter_option_a:
                    if start is None:
                        start = self.start
                    else:
                        start = start + step_size_a
                    param_1, cov_1 = optimize.curve_fit(w.function_run1, x_value, y_value, start)
                    param.append(param_1)
                    cov.append(cov_1)
                    self.start_parameter.append(start)
                    option += 1
            else:
                param, cov = optimize.curve_fit(w.function_run1, x_value, y_value, self.start)

        elif self.function.start == 2:
            if dev_mode is True:
                start1 = None
                option = 0
                param = []
                cov = []
                while option < number_of_parameter_option_a:
                    option2 = 0
                    start2 = None
                    if start1 is None:
                        start1 = self.start[0]
                    else:
                        start1 = start1 + step_size_a
                    while option2 < number_of_parameter_option_b:
                        start = []
                        if start2 is None:
                            start2 = self.start[1]
                        else:
                            start2 = start2 + step_size_b
                        start.append(start1)
                        start.append(start2)
                        try:
                            param_1, cov_1 = optimize.curve_fit(w.function_run2, x_value, y_value, start)#, method='dogbox')
                        except (RuntimeError, ZeroDivisionError) as error:
                            print(error)
                            param_1 = ('failed')
                            cov_1 = ('failed')
                        param.append(param_1)
                        cov.append(cov_1)
                        self.start_parameter.append(start)
                        option2 += 1
                    option += 1
            else:
                param, cov = optimize.curve_fit(w.function_run2, x_value, y_value, self.start)#, method='dogbox')
        elif self.function.start == 3:
            if dev_mode is True:
                start1 = None
                option = 0
                param = []
                cov = []
                while option < number_of_parameter_option_a:
                    if start1 is None:
                        start1 = self.start[0]
                    else:
                        start1 = start1 + step_size_a
                    option2 = 0
                    start2 = None
                    while option2 < number_of_parameter_option_b:
                        if start2 is None:
                            start2 = self.start[1]
                        else:
                            start2 = start2 + step_size_b
                        option3 = 0
                        start3 = None
                        while option3 < number_of_parameter_option_c:
                            start = []
                            if start3 is None:
                                start3 = self.start[2]
                            else:
                                start3 = start3 + step_size_c
                            start.append(start1)
                            start.append(start2)
                            start.append(start3)
                            param_1, cov_1 = optimize.curve_fit(w.function_run3, x_value,
                                                                y_value, start)
                            param.append(param_1)
                            cov.append(cov_1)
                            self.start_parameter.append(start)
                            option3 += 1
                        option2 += 1
                    option += 1
            else:
                param, cov = optimize.curve_fit(w.function_run3, x_value, y_value, self.start)
        elif self.function.start == 4:
            if dev_mode is True:
                start1 = None
                option = 0
                param = []
                cov = []
                while option < number_of_parameter_option_a:
                    if start1 is None:
                        start1 = self.start[0]
                    else:
                        start1 = start1 + step_size_a
                    option2 = 0
                    start2 = None
                    while option2 < number_of_parameter_option_b:
                        if start2 is None:
                            start2 = self.start[1]
                        else:
                            start2 = start2 + step_size_b
                        option3 = 0
                        start3 = None
                        while option3 < number_of_parameter_option_c:
                            if start3 is None:
                                start3 = self.start[2]
                            else:
                                start3 = start3 + step_size_c
                            option4 = 0
                            start4 = None
                            while option4 < number_of_parameter_option_d:
                                start = []
                                if start4 is None:
                                    start4 = self.start[3]
                                else:
                                    start4 = start4 + step_size_d
                                start.append(start1)
                                start.append(start2)
                                start.append(start3)
                                start.append(start4)
                                param_1, cov_1 = optimize.curve_fit(w.function_run4, x_value,
                                                                    y_value, start)
                                self.start_parameter.append(start)
                                param.append(param_1)
                                cov.append(cov_1)
                                option4 += 1
                            option3 += 1
                        option2 += 1
                    option += 1
            else:
                param, cov = optimize.curve_fit(w.function_run4, x_value, y_value, self.start)
        elif self.function.start == 5:
            if dev_mode is True:
                start1 = None
                option = 0
                param = []
                cov = []
                while option < number_of_parameter_option_a:
                    if start1 is None:
                        start1 = self.start[0]
                    else:
                        start1 = start1 + step_size_a
                    option2 = 0
                    start2 = None
                    while option2 < number_of_parameter_option_b:
                        if start2 is None:
                            start2 = self.start[1]
                        else:
                            start2 = start2 + step_size_b
                        option3 = 0
                        start3 = None
                        while option3 < number_of_parameter_option_c:
                            if start3 is None:
                                start3 = self.start[2]
                            else:
                                start3 = start3 + step_size_c
                            option4 = 0
                            start4 = None
                            while option4 < number_of_parameter_option_d:
                                if start4 is None:
                                    start4 = self.start[3]
                                else:
                                    start4 = start4 + step_size_d
                                option5 = 0
                                start5 = None
                                while option5 < number_of_parameter_option_e:
                                    start = []
                                    if start5 is None:
                                        start5 = self.start[4]
                                    else:
                                        start5 = start5 + step_size_e
                                    start.append(start1)
                                    start.append(start2)
                                    start.append(start3)
                                    start.append(start4)
                                    start.append(start5)
                                    param_1, cov_1 = optimize.curve_fit(w.function_run5, x_value,
                                                                        y_value, start)
                                    param.append(param_1)
                                    cov.append(cov_1)
                                    self.start_parameter.append(start)
                                    option5 += 1
                                option4 += 1
                            option3 += 1
                        option2 += 1
                    option += 1
            else:
                param, cov = optimize.curve_fit(w.function_run5, x_value, y_value, self.start)
        else:
            print('this function requires less then 1 or more then 5 parameters to be optimized'
                  'and cannot be handled by the current version of the curve fitter.')
        self.results.append(param)
        self.results.append(cov)
        return


    def analyse_values(self):
        """ calculates and returns statistical key values for the interpretation of the fit"""
        # new y values calculated by the estimated function
        new_y_value = []
        residual = []
        w.current_function = self.function.formula
        for value in range(len(self.x_value+1)):
            if dev_mode == True:
                option = 0
            if self.function.start == 1:
                if dev_mode is True:
                    new_y = []
                    residual1 = []
                    while option < len(self.results[0]):
                        new_y1 = w.function_run1(self.x_value.iloc[value], self.results[0][option])
                        new_y.append(new_y1)
                        residual1.append(self.y_value.iloc[value]-new_y1)
                        option += 1
                    residual.append(residual1)
                else:
                    new_y = w.function_run1(self.x_value.iloc[value], self.results[0][0])
                    residual.append(self.y_value.iloc[value]-new_y)
                new_y_value.append(new_y)
            elif self.function.start == 2:
                if dev_mode is True:
                    new_y = []
                    residual1 = []
                    while option < len(self.results[0]):
          #              print(self.results[0][option][0])
                        if self.results[0][option][0] == 'f':
                            new_y.append('failed')
                            residual1.append('failed')
                        else:
                            new_y1 = w.function_run2(self.x_value.iloc[value], self.results[0][option][0],
                                                     self.results[0][option][1])
                            new_y.append(new_y1)
                            residual1.append(self.y_value.iloc[value]-new_y1)
                        option += 1
                    residual.append(residual1)
                else:
                    new_y = w.function_run2(self.x_value.iloc[value], self.results[0][0], self.results[0][1])
                    residual.append(self.y_value.iloc[value]-new_y)
                new_y_value.append(new_y)
            elif self.function.start == 3:
                if dev_mode is True:
                    new_y = []
                    residual1 = []
                    while option < len(self.results[0]):
                        try:
                            new_y1 = w.function_run3(self.x_value.iloc[value], self.results[0][option][0],
                                                 self.results[0][option][1], self.results[0][option][2])
                            new_y.append(new_y1)
                        except ZeroDivisionError:
                            new_y.append(0)
                            new_y1 = 0
                        residual1.append(self.y_value.iloc[value] - new_y1)
                        option += 1
                    residual.append(residual1)
                else:
                    new_y = w.function_run3(self.x_value.iloc[value], self.results[0][0],
                                            self.results[0][1], self.results[0][2])
                    residual.append(self.y_value.iloc[value] - new_y)
                new_y_value.append(new_y)
            elif self.function.start == 4:
                if dev_mode is True:
                    new_y = []
                    residual1 = []
                    while option < len(self.results[0]):
                        new_y1 = w.function_run4(self.x_value.iloc[value], self.results[0][option][0],
                                                 self.results[0][option][1], self.results[0][option][2],
                                                 self.results[0][option][3])
                        new_y.append(new_y1)
                        residual1.append(self.y_value.iloc[value] - new_y1)
                        option += 1
                    residual.append(residual1)
                else:
                    new_y = w.function_run4(self.x_value.iloc[value], self.results[0][0],
                                            self.results[0][1], self.results[0][2],
                                            self.results[0][3])
                    residual.append(self.y_value.iloc[value] - new_y)
                new_y_value.append(new_y)
            elif self.function.start == 5:
                if dev_mode is True:
                    new_y = []
                    residual1 = []
                    while option < len(self.results[0]):
                        new_y1 = w.function_run5(self.x_value.iloc[value], self.results[0][option][0],
                                                 self.results[0][option][1], self.results[0][option][2],
                                                 self.results[0][option][3], self.results[0][option][4])
                        new_y.append(new_y1)
                        residual1.append(self.y_value.iloc[value] - new_y1)
                        option += 1
                    residual.append(residual1)
                else:
                    new_y = w.function_run5(self.x_value.iloc[value], self.results[0][0],
                                            self.results[0][1], self.results[0][2],
                                            self.results[0][3], self.results[0][4])
                    residual.append(self.y_value.iloc[value] - new_y)
                new_y_value.append(new_y)
        self.ny_value = pd.Series(new_y_value, copy=False)
        self.residuals = pd.Series(residual, copy=False)

        # calculation of not parameter specific results

        if dev_mode == True:
            option = 0
            r_squared = []
            ad_r_squared = []

            while option < len(self.results[0]):
                sse = 0  # sum of squares of the regression
                sst = 0  # total sum of square
                for count in range(len(self.x_value+1)):
             #       print(1, self.ny_value[count][option])
                    if self.ny_value[count][option] == 'failed':
              #          print('here')
                        sse = 'failed'
                        sst = 'failed'
                        break
                    sse = sse + (self.y_value.iloc[count] - self.ny_value[count][option]) ** 2
                    sst = sst + (self.y_value.iloc[count] - self.y_value.mean()) ** 2
            #    print(3)
                if sse and sst == 'failed':
                    r_squared.append('failed')
                    ad_r_squared.append('failed')
                else:
                    r_squared.append(1 - sse/sst)
                    ad_r_squared.append(1-(1-(1-sse/sst))*((len(self.x_value)-1)/(len(self.x_value)-self.function.start)))
                option += 1

            self.results.append(r_squared)      # results[2]    only in dev_mode!
            self.results.append(ad_r_squared)   # results[3]    only in dev_mode!
            return
        else:
            sse = 0  # sum of squares due to error
            ssr = 0  # sum of squares of the regression
            sst = 0  # total sum of squares
            for count in range(len(self.x_value + 1)):
                sse = sse + (self.y_value.iloc[count] - self.ny_value.iloc[count]) ** 2
                ssr = ssr + (self.ny_value.iloc[count] - self.y_value.mean()) ** 2
                sst = sst + (self.y_value.iloc[count] - self.y_value.mean()) ** 2

        ss = (sse, ssr, sst)
        r_squared = 1 - sse / sst
        ad_r_squared = 1-(1-r_squared)*((len(self.x_value)-1)/
                                        (len(self.x_value)-self.function.start))

        df = len(self.x_value) - 1  # degrees of freedom
        mse = sse / (df + 1)        # mean square error
        rmse = np.sqrt(mse)         # root mean square error
        # critical t-value for finding the confidence intervals for the parameters
        t_value = stats.t.ppf(1 - 0.025, df)

        # calculation of parameter specific results
        var = []        # list for the variance of the parameters
        for para_count in range(len(self.results[0])):
            var.append(self.results[1][para_count][para_count])
        std_err = np.sqrt(np.diag(self.results[1]))     # list for the standard error of the parameters
        con = t_value * np.sqrt(var)                    # list of the confidence intervals of the parameters

        # confidence intervalls
        step_size = (max(self.x_value) - min(self.x_value)) / (len(self.x_value) * 2)
        low_bound = []
        up_bound = []
        sum_var = sum(var)
        for con_x in np.arange(min(self.x_value) - step_size * 3,
                               max(self.x_value) + step_size * 3, step_size):
            if self.function.start == 1:
                con_y = w.function_run1(con_x, self.results[0])
            elif self.function.start == 2:
                con_y = w.function_run2(con_x, self.results[0][0], self.results[0][1])
            elif self.function.start == 3:
                con_y = w.function_run3(con_x, self.results[0][0], self.results[0][1], self.results[0][2])
            elif self.function.start == 4:
                con_y = w.function_run4(con_x, self.results[0][0], self.results[0][1], self.results[0][2], self.results[0][3])
            elif self.function.start == 5:
                con_y = w.function_run5(con_x, self.results[0][0], self.results[0][1], self.results[0][2], self.results[0][3], self.results[0][4])
            low_bound.append(con_y - t_value * np.sqrt(mse+sum_var))
            up_bound.append(con_y + t_value * np.sqrt(mse+sum_var))
        self.low_bound = low_bound
        self.up_bound = up_bound
    #    print(self.low_bound)

        # put everything together in self.results
        # parameters = results[0], covariance = results[1]
        self.results.append(var)                # results[2]
        self.results.append(std_err)            # results[3]
        self.results.append(r_squared)          # results[4]
        self.results.append(ad_r_squared)       # results[5]
        self.results.append(ss)                 # results[6] list with sse, ssr and sst
        self.results.append(df)                 # results[7]
        self.results.append(t_value)            # results[8]
        self.results.append(con)                # results[9]
        self.results.append(rmse)               # results[10]
