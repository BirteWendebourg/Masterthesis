""" function to convert the units that are known to the curve converter """


# gets header of the column that has to be converted
# start unit and goal unit
# dataframe with input data

def check_units(units, number_of_columns):
    """checks if all units are there and valid, known units"""
    # erstmal nur ob alle units ausgewählt wurden
    if len(units) != number_of_columns:
        return None, 2
    for unit in units:
        if unit == '':
            return None, 2
    return units, 0


class ConUnit:
    """connection to the unit converter"""
    def __init__(self):
        return

    def converter(self):
        """converts a unit into a different one, under construction"""
        return