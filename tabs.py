""" create a tab for each step of the analysis"""
# gui imports
import tkinter as tk
from tkinter import ttk
# imports for the data handling
from tkinter import filedialog
# graphic imports
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
import statsmodels.api as sm
import numpy as np
import pandas as pd
# import brewer2mpl
# from brewer2mpl import qualitative
# own inputs
import widgets as w

"""adding a developers option"""
dev_mode = False
# activates the developer mode in which different parameters can be tested and documented easily
# data loading and selection is still the same as in the normal mode
'TODO: get it from the gui class'

matplotlib.use('TkAgg')

'TO DO: change in to a more general class and use multiple times'


class Tabs(ttk.Notebook):
    """ creates tabs for the different parts of the program """
    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)
        self.parent = parent
        self.tab_control = ttk.Notebook(parent)
        # data tab to manage the input data set
        self.data_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.data_tab, text='Data')
        # analysis tab to run the analyses
        self.analyse_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.analyse_tab, text='Analysis')
        # result tab to view the results of the current analyses
        self.result_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.result_tab, text='Results')
        # overview tab with summary of all analyse runs
        self.overview_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.overview_tab, text='Overview')
        self.tab_control.pack(expand=1, fill="both")

        # data_tab start set up
        self.set_up_data_tab(0)

        # analyse_tab start set up
        self.style = ttk.Style()
        self.x_box = None
        self.y_box = None
        self.set_up_analyse_tab()

        # result_tab start set up
        self.set_up_result_tab(True)

        # overview_tab start set up
        tk.Label(self.overview_tab,
                 text='In Progress:\n'
                      'Will show an overview over all past analyses '
                      'that have been performed so far.').pack(side='top')

    def set_up_data_tab(self, call):
        """sets up the data tab
        the variable call tells the function
        if data is being loaded or if the start screen is needed"""
        if call == 0:
            init_load = tk.Button(master=self.data_tab, text='load new data',
                                  command=self.parent.con_d.load)
            init_load.pack(side=tk.TOP, expand=tk.YES)
            reload = tk.Button(master=self.data_tab, text='load processed data',
                               command=self.parent.con_d.reload)
            reload.pack(side=tk.TOP, expand=tk.YES)
            return
        for widget in self.data_tab.winfo_children():
            widget.destroy()
        self.parent.show(self.data_tab, self.parent.con_d.input_data)
        return

    def set_up_analyse_tab(self):
        """ set up of the analysis tab """
        if self.parent.con_d.data is None:
            analyse_frame = tk.Frame(self.analyse_tab)
            analyse_frame.pack()
            tk.Label(analyse_frame, text='please load in data before performing an analysis')\
                .pack(side='top')
            return
        for widget in self.analyse_tab.winfo_children():
            widget.destroy()

        # create a set-up of frames to organize the structure
        # data selection
        frame1 = tk.Frame(self.analyse_tab)
        frame1.pack(fill=tk.X)
        tk.Label(frame1, text='Select the data for the analyses run:', width=31)\
            .pack(side=tk.LEFT, padx=5, pady=5)

        frame2 = tk.Frame(self.analyse_tab)
        frame2.pack(fill=tk.X)
        tk.Label(frame2, text='x_values:', width=10).pack(side=tk.LEFT, padx=5, pady=5)
        self.parent.con_a.x_values_selection = tk.StringVar()
        self.x_box = ttk.Combobox(frame2, textvariable=self.parent.con_a.x_values_selection,
                                  style='check_x.TCombobox')
        self.x_box['values'] = self.parent.con_d.data.headers
        self.x_box['state'] = 'readonly'
        self.x_box.bind("<<ComboboxSelected>>", self.check_x_column)
        self.x_box.pack(fill=tk.X, padx=5, expand=tk.TRUE)

        frame3 = tk.Frame(self.analyse_tab)
        frame3.pack(fill=tk.X)
        tk.Label(frame3, text='y_values:', width=10).pack(side=tk.LEFT, padx=5, pady=5, anchor='n')
        self.parent.con_a.y_values_selection = tk.StringVar()
        self.y_box = ttk.Combobox(frame3, textvariable=self.parent.con_a.y_values_selection,
                                  style='check_y.TCombobox')
        self.y_box['values'] = self.parent.con_d.data.headers
        self.y_box['state'] = 'readonly'
        self.y_box.bind("<<ComboboxSelected>>", self.check_y_column)
        self.y_box.pack(fill=tk.X, padx=5, expand=tk.TRUE)

        tk.Button(frame3, text="Show data points", command=self.show_raw).pack(side=tk.RIGHT,
                                                                           padx=5, pady=5)

        # function selection
        frame4 = tk.Frame(self.analyse_tab)
        frame4.pack(fill=tk.X)
        tk.Label(frame4, text='Select a type of function for the analyse run:', width=38) \
            .pack(side=tk.LEFT, padx=5, pady=5)

        frame5 = tk.Frame(self.analyse_tab)
        frame5.pack(fill=tk.X)
        for counter in range(len(self.parent.con_a.ana.kinds)):
            text = self.parent.con_a.ana.kinds[counter] + ' analysis'
            button = tk.Button(master=frame5, text=text,
                               command=self.wrap_function(counter))
            button.pack(side=tk.LEFT, expand=tk.YES)

        # create frames to structure additional input information
        tk.Label(self.analyse_tab, text='\nChoose the functions:', width=15,
                 padx=20).pack(side='top', anchor='w')

        # create the command button to confirm and load the input information
        frame6 = tk.Frame(self.analyse_tab)
        frame6.pack(side='bottom')
        tk.Button(frame6, text="Run Analyses", command=self.run_analyse).pack(side='left',
                                                                              padx=10, pady=5)
        # create the command button to add another function into the program
        tk.Button(frame6, text="Add New Function").pack(side='right', padx=10, pady=5)
        # , command=self.parent.con_a.add_function)
        return

    def set_up_result_tab(self, analyse):
        """ set up of the result tab depending on the progress of the analyses """
        # set up of the result tab
        'TODO: check why it is not working for processed data, only for new'
        if analyse is True and len(self.parent.con_a.run) == 0:
            # show the results of an analysis? (otherwise only the original data is presented)
            result_frame = tk.Frame(self.result_tab)
            result_frame.pack()
            tk.Label(result_frame, text='In Progress:\n'
                                        'Will show the results of the current analyses.\n'
                                        'Please perform analyses to see any results.')\
                .pack(side='top')
            return

        for widget in self.result_tab.winfo_children():
            widget.destroy()

        # set up the main structure
        frame1 = tk.Frame(self.result_tab)
        frame1.pack(side=tk.LEFT)  # , expand=tk.TRUE)

        frame2 = tk.Frame(self.result_tab)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT)  # , expand=tk.TRUE)

        # graph set up
        # original data + fitted functions
        self.parent.con_a.figure = plt.Figure()
        graph_space = FigureCanvasTkAgg(self.parent.con_a.figure, master=frame1)
        graph = self.parent.con_a.figure.add_subplot(111)
        graph.plot(self.parent.con_a.con_data.data.datatable[
                       self.parent.con_a.x_values_selection.get()].iloc[2:],
                   self.parent.con_a.con_data.data.datatable[
                       self.parent.con_a.y_values_selection.get()].iloc[2:],
                   marker='o', color="#000000", linestyle='None')

        # evaluation graph (QQ-Plot or residual distribution)
        res_figure = plt.Figure()
        res_graph_space = FigureCanvasTkAgg(res_figure, master=frame1)
        res_graph = res_figure.add_subplot(111)

        if analyse is False:
            # the original data is shown
            # the evaluation graph shows if the data has a normal distribution
            sm.qqplot(self.parent.con_a.con_data.data.datatable[
                          self.parent.con_a.y_values_selection.get()].iloc[2:],
                      ax=res_graph, markerfacecolor="#000000", markeredgecolor="#000000")
            res_graph.set_title('QQ-Plot')
            res_graph.grid()


        if analyse is True:
            # the original data and the fitted function is shown
            # the evaluation graph shows the distribution of the residuals
            para_name = ['a', 'b', 'c', 'd', 'e']
            colors = ("#000000", "#004949", "#6db6ff", "#920000", "#490092", "#db6d00",
                      "#24ff24", "#ffff6d", "#009292", "#ff6db6", "#006ddb", "#b6dbff", "#924900",
                      "#b66dff", "#ffb6db")  # list of colorblind friendly colors
            color_count = 1
            for result in self.parent.con_a.run:
                result.analyse_values()

                # residual graph
                res_graph.plot(result.x_value, result.residuals, marker='o',
                               color=colors[color_count], linestyle='None')

                # filling the graph
                graph = self.draw_graph(result, colors, color_count, graph)

                # set up of the numeric feedback section
                frame3 = tk.Frame(frame2)
                frame3.pack(fill=tk.X)
                tk.Label(frame3, text='\n'+result.function.name+'\n'+result.function.formula,
                         fg=colors[color_count]).pack(side='top')
                frame4 = tk.Frame(frame3)
                frame4.pack(side=tk.LEFT)
                frame5 = tk.Frame(frame3)
                frame5.pack(side=tk.LEFT)
                frame6 = tk.Frame(frame3)
                frame6.pack(side=tk.LEFT)
                frame7 = tk.Frame(frame3)
                frame7.pack(side=tk.LEFT)
                frame8 = tk.Frame(frame3)
                frame8.pack(side=tk.LEFT)
                frame9 = tk.Frame(frame3)
                frame9.pack(side=tk.LEFT)
                frame10 = tk.Frame(frame3)
                frame10.pack(side=tk.LEFT)

                tk.Label(frame4, text='').pack(side='top', anchor='w')
                tk.Label(frame5, text='').pack(side='top', anchor='e')
                tk.Label(frame6, text='variance').pack(side='top', padx=5, anchor='e')
                tk.Label(frame7, text='std_err').pack(side='top', padx=5, anchor='e')
                tk.Label(frame8, text='conf_interval 95%').pack(side='top', padx=5, anchor='e')
                tk.Label(frame9, text='R-square:').pack(side='top', padx=20, anchor='w')
                tk.Label(frame9, text='adjusted R-squared:').pack(side='top', padx=20, anchor='w')
                if result.results[4] < 0:
                    tk.Label(frame10, foreground='red', text=('{:.2f}'.format(result.results[4])))\
                        .pack(side='top', padx=20, anchor='e')
                else:
                    tk.Label(frame10, text=('{:.2f}'.format(result.results[4]))) \
                        .pack(side='top', padx=20, anchor='e')
                if result.results[5] < 0:
                    tk.Label(frame10, foreground='red', text=('{:.3f}'.format(result.results[5]))) \
                        .pack(side='top', padx=20, anchor='e')
                else:
                    tk.Label(frame10, text=('{:.3f}'.format(result.results[5]))) \
                        .pack(side='top', padx=20, anchor='e')

                for para_count in range(len(result.results[0])):
                    tk.Label(frame4, text=para_name[para_count]).pack(side='top', anchor='w')
                    tk.Label(frame5, text=('{:.2f}'.format(result.results[0][para_count])))\
                        .pack(side='top', anchor='e')
                    tk.Label(frame6, text=('+/- {:.2f}'.format(result.results[2][para_count]))) \
                        .pack(side='top', anchor='e')
                    tk.Label(frame7, text=('{:.2f}'.format(result.results[3][para_count])))\
                        .pack(side='top', anchor='e')
                    tk.Label(frame8, text=('({:.2f}, {:.2f})'.format(
                        (result.results[0][para_count] - result.results[9][para_count]),
                        (result.results[0][para_count] + result.results[9][para_count]))))\
                        .pack(side='top', anchor='e')

                res_graph.set_xlabel(self.parent.con_a.x_values_selection.get() + ' [' +
                                     self.parent.con_d.data.datatable[
                                         self.parent.con_a.x_values_selection.get()].iloc[0] + ']')
                res_graph.set_ylabel('residuals' + ' [' + self.parent.con_d.data.datatable[
                    self.parent.con_a.y_values_selection.get()].iloc[0] + ']')
                res_graph.set_title('residuals')
                res_graph.grid()

                color_count += 1

            # set axis limits
            x_steps = (max(self.parent.con_a.x_values) - min(self.parent.con_a.x_values)) / \
                      (len(self.parent.con_a.x_values) * 2)
            y_steps = (max(self.parent.con_a.y_values) - min(self.parent.con_a.y_values)) / \
                      (len(self.parent.con_a.y_values) * 2)
            x_lim = min(self.parent.con_a.x_values) - x_steps * 2, max(self.parent.con_a.x_values) + x_steps * 2
            y_lim = min(self.parent.con_a.y_values) - y_steps * 2, max(self.parent.con_a.y_values) + y_steps * 2
            graph.set_xlim(x_lim)
            graph.set_ylim(y_lim)

        # draw graph
        graph.set_xlabel(self.parent.con_a.x_values_selection.get() + ' [' +
                         self.parent.con_d.data.datatable[
                             self.parent.con_a.x_values_selection.get()].iloc[0] + ']')
        graph.set_ylabel(self.parent.con_a.y_values_selection.get() + ' [' +
                         self.parent.con_d.data.datatable[
                             self.parent.con_a.y_values_selection.get()].iloc[0] + ']')
        graph.set_title('resulting functions')
        graph.grid()
        graph_space.draw()
        graph_space.get_tk_widget().pack(side=tk.TOP)

        res_graph_space.draw()
        res_graph_space.get_tk_widget().pack(side=tk.TOP)
        return

    # """small helper functions"""
    def wrap_function(self, counter):
        """lambda function wrapper"""
        # this wrapper is necessary because otherwise lambda will look for the value of counter
        # when the function is called which will be after the for-loop that allows for a dynamic
        # function call, depending on the amount of different analyse types known by the program
        return lambda: self.parent.con_a.analyse_set_up(counter)

    def run_analyse(self):
        """ wrapper function to kick of all functions involved in the performance of the analysis
         and presentation of the results"""
        # check if columns were selected and if the selected data can be analysed
        # (no strings in the data etc)
        if self.check_data() is False:
            return 1

        # check if at least one function was selected
        choice_count = sum(count.get() for count in self.parent.con_a.function_choice)
        if choice_count == 0:
            select_func_error = tk.Toplevel()
            select_func_error.title("Function Selection Error")
            select_func_error.geometry('300x100')
            tk.Label(select_func_error,
                     text="\nPlease select at least one function\n").pack(side='top')
            select_func_error_close = tk.Button(select_func_error, text="Ok",
                                                command=select_func_error.destroy)
            select_func_error_close.pack()
            return 1

        # evaluate the selection in the analysis tab and run the analysis
        self.parent.con_a.process_ana_tab(choice_count)

        if dev_mode is True:
            for run in self.parent.con_a.run:
                run.analyse_values()
            self.dev_save()
        else:
            # refresh the result tab to show the results
            self.set_up_result_tab(True)
            # jump to the result tab
            self.tab_control.select('.!notebook.!frame3')

    def save_graph(self):
        """ save the graph at the chosen location """
        colors = ("#000000", "#004949", "#6db6ff", "#920000", "#490092", "#db6d00",
                  "#24ff24", "#ffff6d", "#009292", "#ff6db6", "#006ddb", "#b6dbff", "#924900",
                  "#b66dff", "#ffb6db")  # list of colorblind friendly colors
        color_count = 1

        # graph set up
        graph = self.parent.con_a.figure.add_subplot(111)
        graph.plot(self.parent.con_a.con_data.data.datatable[
                       self.parent.con_a.x_values_selection.get()].iloc[2:],
                   self.parent.con_a.con_data.data.datatable[
                       self.parent.con_a.y_values_selection.get()].iloc[2:],
                   marker='o', color="#000000", linestyle='None')

        for result in self.parent.con_a.run:
            graph = self.draw_graph(result, colors, color_count, graph)
            color_count += 1

        #define limits
        x_steps = (max(self.parent.con_a.x_values) - min(self.parent.con_a.x_values)) / \
                  (len(self.parent.con_a.x_values) * 2)
        y_steps = (max(self.parent.con_a.y_values) - min(self.parent.con_a.y_values)) / \
                  (len(self.parent.con_a.y_values) * 2)
        x_lim = min(self.parent.con_a.x_values) - x_steps * 2, max(self.parent.con_a.x_values) + x_steps * 2
        y_lim = min(self.parent.con_a.y_values) - y_steps * 2, max(self.parent.con_a.y_values) + y_steps * 2
        graph.set_xlim(x_lim)
        graph.set_ylim(y_lim)

        graph.legend()

        figure_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                   filetypes=(("PNG file", "*.png"),
                                                              ("JPEG file", "*.jpeg"),
                                                              ("PDF file", "*.pdf")))
        with open(figure_path, mode='wb') as stream:
            self.parent.con_a.figure.savefig(stream)

    def check_x_column(self, event):
        self.x_box.selection_clear()
        column_type = self.parent.con_d.data.data_types.get(
            self.parent.con_a.x_values_selection.get())
        if column_type == 'int64' or column_type == 'float64':
            self.style.map('check_x.TCombobox', foreground=[('readonly', 'black')])
        else:
            self.style.map('check_x.TCombobox', foreground=[('readonly', 'red')])

    def check_y_column(self, event):
        self.y_box.selection_clear()
        column_type = self.parent.con_d.data.data_types.get(
            self.parent.con_a.y_values_selection.get())
        if column_type == 'int64' or column_type == 'float64':
            self.style.map('check_y.TCombobox', foreground=[('readonly', 'black')])
        else:
            self.style.map('check_y.TCombobox', foreground=[('readonly', 'red')])

    def check_data(self):
        """ check if columns were selected and if the selected data can be analysed
        (no strings in the data etc) """
        column_x_type = self.parent.con_d.data.data_types.get(
            self.parent.con_a.x_values_selection.get())
        column_y_type = self.parent.con_d.data.data_types.get(
            self.parent.con_a.y_values_selection.get())
        if (column_x_type != 'int64' and column_x_type != 'float64') \
                or (column_y_type != 'int64' and column_y_type != 'float64'):
            selection_error = tk.Toplevel()
            selection_error.title("Column Selection Error")
            selection_error.geometry('275x125')
            tk.Label(selection_error,
                     text="\nPlease select numerical columns\n of the type float or int!\n"
                          "Unusable columns are indicated in red.",
                     wraplength=250, justify=tk.CENTER).pack(side='top')
            selection_error_close = tk.Button(selection_error, text="Ok",
                                              command=selection_error.destroy)
            selection_error_close.pack()
            return False
        return True

    def show_raw(self):
        """ show the data points without any analysis being performed """
        # check if columns were selected and if the selected data can be analysed
        # (no strings in the data etc)
        if self.check_data() is False:
            return 1
        # refresh the result tab to show the plot
        self.set_up_result_tab(False)
        # jump to the result tab
        self.tab_control.select('.!notebook.!frame3')

    def draw_graph(self, result, colors, color_count, graph):
        # result = analysis run from which the results should be drawn
        # colors = color blind friendly selection of colors
        # color_count = how many functions have already been drawn, which color should be used now
        # graph = subplot in which to draw
        # setting the global variable to the current function
        w.current_function = result.function.formula
        # dynamically defining the step size
        step_size = (max(self.parent.con_a.x_values) - min(self.parent.con_a.x_values)) / \
                    (len(self.parent.con_a.x_values) * 2)
        if result.function.start == 1:
             graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                        w.function_run1(np.arange(
                            min(self.parent.con_a.x_values) - step_size * 3,
                            max(self.parent.con_a.x_values) + step_size * 3, step_size),
                            result.results[0][0]), color=colors[color_count], linewidth=4, label=result.function.name)
        elif result.function.start == 2:
             graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                       w.function_run2(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                                        result.results[0][0], result.results[0][1]), color=colors[color_count],
                        linewidth=4, label=result.function.name)
        elif result.function.start == 3:
             graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                        w.function_run3(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                                        result.results[0][0], result.results[0][1],
                                        result.results[0][2]), color=colors[color_count], linewidth=4, label=result.function.name)
        elif result.function.start == 4:
             graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                        w.function_run4(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                                        result.results[0][0], result.results[0][1],
                                        result.results[0][2], result.results[0][3]), color=colors[color_count],
                        linewidth=4, label=result.function.name)
        elif result.function.start == 5:
             graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                  max(self.parent.con_a.x_values) + step_size * 3, step_size),
                        w.function_run5(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                                                 max(self.parent.con_a.x_values) + step_size * 3, step_size),
                                        result.results[0][0], result.results[0][1],
                                        result.results[0][2], result.results[0][3],
                                        result.results[0][4]), color=colors[color_count], linewidth=4, label=result.function.name)
        else:
             print('found invalid analysis')
   #     print(result.low_bound)
        graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                             max(self.parent.con_a.x_values) + step_size * 3, step_size),
                   result.low_bound, linestyle='dashed', color=colors[color_count], linewidth=2)
        graph.plot(np.arange(min(self.parent.con_a.x_values) - step_size * 3,
                             max(self.parent.con_a.x_values) + step_size * 3, step_size),
                   result.up_bound, linestyle='dashed', color=colors[color_count], linewidth=2)
        return graph

    def dev_save(self):
        adj = True

        if adj == True:
            header = True
            result_table = pd.DataFrame()
            for run in self.parent.con_a.run:
                adR_lines = []
                if header == True:
                    adR_line = [run.start_parameter[0][0]]
                else:
                    adR_line = []
                line1 = ['a/b']
                line_set = set()
                prev_para = run.start_parameter[0][0]
                for run_count in range(len(run.results[0])):
                    if run.start_parameter[run_count][1] not in line_set:
                        line_set.add(run.start_parameter[run_count][1])
                        line1.append(run.start_parameter[run_count][1])
     #                   print(line1)
                    adR = run.results[3][run_count]
                    if run.start_parameter[run_count][0] != prev_para:
                        adR_lines.append(adR_line)
                        adR_line = []
                        if header == True:
                            adR_line.append(run.start_parameter[run_count][0])
                        adR_line.append(adR)
                        prev_para = run.start_parameter[run_count][0]
                    else:
                        adR_line.append(adR)
                head_line = []
                adR_lines.append(adR_line)
                if header == True:
                    head_line.append(line1)
                header_table = pd.DataFrame(data=head_line)
                data_table = pd.DataFrame(data=adR_lines)
                result_table = pd.concat([result_table, header_table, data_table])
        if adj == False:
            # collect and sort all the information that should be saved
            para_name = ('a', 'b', 'c', 'd', 'e')
            result_table = pd.DataFrame()
            for run in self.parent.con_a.run:
                line1 = ('Function: ', run.function.name, 'Formula: ', run.function.formula)
                data_table = pd.DataFrame()
                for run_count in range(len(run.results[0])):
                    line2 = (run_count+1, '', '', '')
                    line3 = ('Parameter: ', 'Start: ', 'Estimated: ', '')
                    para_lines = []
                    for para_count in range(run.function.start):
                        para_line = []
                        para_line.append(para_name[para_count])
                        para_line.append(run.start_parameter[run_count][para_count])
                        para_line.append(run.results[0][run_count][para_count])
                        para_lines.append(para_line)
                    line4 = ('adjusted R-square: ', run.results[3][run_count])
          #      line4 = ('R-square: ', run.results[2][run_count], 'adjusted R-square: ', run.results[3][run_count])
                    para_lines.append(line4)
                    if len(data_table) == 0:
                        counter_table = pd.DataFrame(data=(line1, line2, line3))
                    else:
                        counter_table = pd.DataFrame(data=(line2, line3))
                    para_table = pd.DataFrame(data=para_lines)
                    data_table = pd.concat([data_table, counter_table, para_table])
                result_table = pd.concat([result_table, data_table])

        # get file path and save the table
        result_path = filedialog.asksaveasfilename(filetypes=[('Comma Separated Values', '*.csv')])
        if len(result_path) == 0:
            return 0
        with open(result_path, mode='w') as stream:
            result_table.to_csv(stream, index=False)
        return 0
