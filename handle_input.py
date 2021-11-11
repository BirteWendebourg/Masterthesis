import re
import sys
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import ttk


def open_data():
    # asks the user for the input file
    filepath = filedialog.askopenfilename()
    print(filepath)

    if len(filepath) == 0:
        print(0)
        return 0
    else:
    # Toplevel object which will be treated as a new window
        window = Toplevel()

    # sets the title and geometry of the window
        window.title("Load Data")
        window.geometry("200x200")

    #    load = Button(data_tab, text="Test", bg="red", fg="black", command=save(0))
# button1.grid()

        # attempt to open the file
        try:
            stream = open(filepath)
        except IOError as err:
            sys.stderr.write('{}: cannot open file {}\n'.format(sys.argv[0], filepath))
            exit(1)

        stream.close()



  #  filepath = filedialog.askopenfilename()

    # A Label widget to show in toplevel
   # Label(window, text="This is a new window").pack()


def data_table_new(lines):
    data = pd.read_csv(lines)
    datatable = pd.DataFrame(data)
    return datatable


def get_tasks():
    return 0


def next_action(new_tasks):
    if new_tasks == 1:
        return True


def save():
    output = 0
    if output == 0:
        return 0
    else:
        export_csv = output.to_csv('results.csv', index=False, header=True)
    return 0
