# David Jantz
# 7/29/24
# Github: David2847
# Description: This script moves checkbook data around in a CSV file for easier processing.

import csv


class Income:

    def __init__(self, all_transactions):
        """ Take in a checkbook object. Extracts only positive values into a list of dicts."""
        self._data_list = []
        for row in all_transactions.get_data_list():
            if float(row['Amount']) > 0:
                self._data_list.append(row)
        # self.display()

    def display(self):
        """ Display the current data structure for testing purposes."""
        for row in self._data_list:
            print(row)

    def revise_column_titles(self):
        """ Renames column titles to their new names. Ignores columns to be deleted."""
        # Mapping of old keys to new keys
        # todo: this key_mapping is unfinished! Also maybe it really only needs to handle Amount.
        key_mapping = {
            'Amount': 'Total Amount',
            'Category': 'Copays'
        }

        for row_num in range(len(self._data_list)):
            new_row = {key_mapping.get(k, k): v for k, v in self._data_list[row_num].items()}
            self._data_list[row_num] = new_row

    def write_to_csv(self):
        column_titles = self.get_column_titles()

        # name of csv file
        filename = "income.csv"

        # writing to csv file
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=column_titles)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows(self._data_list)

    def get_column_titles(self):
        headers = []
        for key in self._data_list[0].keys():
            headers.append(key)
        return headers

    def add_columns(self):
        for row in self._data_list:
            row['Copays'] = ''
            row['Third Party Payments'] = ''
            row['Refunds Received'] = ''
            row['Transfers Received'] = ''

    def categorize_payments(self):
        # four new columns: copays, third party payments, refunds received, transfers received
        self.add_columns()

        for row in self._data_list:
            # if category column has D: Amount -> copays
            if 'D' in row['Category']:
                row['Copays'] = row['Amount']
            # if category column has E: Amount -> Third Party Payments
            elif 'E' in row['Category']:
                row['Third Party Payments'] = row['Amount']
            # if category column has D: Amount -> copays
            elif 'F' in row['Category']:
                row['Refunds Received'] = row['Amount']
            # if category column has E: Amount -> Third Party Payments
            elif 'G' in row['Category']:
                row['Transfers Received'] = row['Amount']
            # if category column is empty: that means the amount is split. iterate through row until finding a D.
            # then move the value to the right of it into Copays. keep iterating through until finding an E. then
            # move the value to the right of it into Third Party Payments. Same for F and G. that should be it.
            else:
                for value in row.values():
                    ok, this is where I need to index the dictionary as I search it so that I can grab the value to the right



class Expenses:
    pass


class InitialCheckbook:
    """ Parent class for everything... Reads into python data object, does initial data manipulation,
    then splits data into income and expenses objects. """

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
    transactions = InitialCheckbook('april_input.csv')
    # reformat dates into integers, this is required for both income and expenses
    transactions.dates_to_day_numbers()
    # split data into income and expenses
    income = Income(transactions)
    # take care of columns D and E based on adjacent letter. makes new columns at the end.
    #       Theoretically also handles F and G.
    income.categorize_payments()
    # rename columns
    # remove extra columns
    # Write to csv
    income.write_to_csv()


    """
    income:
        take care of yellow highlighted edge cases in excel file
        maybe do a check to make sure total amount is actually the sum of the others
        output to new csv file
    expenses:
        reorder / rename / add headers
        make amounts positive
    """


if __name__ == "__main__":
    main()
