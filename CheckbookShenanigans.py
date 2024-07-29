# David Jantz
# 7/29/24
# Github: David2847
# Description: This script moves checkbook data around in a CSV file for easier processing.

import csv

"""
open up csv file, store in a list of dicts
stuff for both data and expenses:
    reformat dates into integers
split data into income and expenses
income:
    remove check no column and others
    rename headers
    take care of columns D and E based on adjacent letter
    take care of yellow highlighted edge cases in excel file
    maybe do a check to make sure total amount is actually the sum of the others
    output to new csv file
expenses:
    reorder / rename / add headers
    make amounts positive
"""


class Income:
    pass


class Expenses:
    pass


class Checkbook:
    def __init__(self, input_file):
        """
        Opens input data file, reads it into a list of dicts where each dict is a row
            and the keys are the column headers.
        """
        with open('april_input.csv', mode='r', newline='', encoding='utf-8-sig') as input_file:
            csv_reader = csv.DictReader(input_file)
            self._data_list = []

            # reader = csv.reader(input_file)
            for row in csv_reader:
                self._data_list.append(row)

        # self.display()

    def get_data_list(self):
        return self._data_list

    def display(self):
        """ Display the current data structure for testing purposes."""
        for row in self._data_list:
            print(row)

    def dates_to_day_numbers(self):
        """ Turns mm/dd/yyyy into string day numbers """
        for row in self._data_list:
            new_date_string = ''
            date = row['Date']
            on_day_number = False
            # iterate through the string, flip from not appending char to new string to appending
            #       every time we hit a slash.
            for char in date:
                if char == '/':
                    on_day_number = not on_day_number
                elif on_day_number:
                    new_date_string = new_date_string + char
            row['Date'] = new_date_string
        # self.display()



def main():
    # open up csv file, store in a list of dicts
    checkbook = Checkbook('april_input.csv')
    # reformat dates into integers, this is required for both income and expenses
    checkbook.dates_to_day_numbers()
    # split data into income and expenses


    """
    income:
        remove check no column and others
        rename headers
        take care of columns D and E based on adjacent letter
        take care of yellow highlighted edge cases in excel file
        maybe do a check to make sure total amount is actually the sum of the others
        output to new csv file
    expenses:
        reorder / rename / add headers
        make amounts positive
    """


if __name__ == "__main__":
    main()
