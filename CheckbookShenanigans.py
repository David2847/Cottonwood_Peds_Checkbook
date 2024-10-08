# David Jantz
# 7/29/24
# Github: David2847
# Description: This script moves checkbook data around in a CSV file for easier processing.

import csv


class Income:

    def __init__(self, all_transactions):
        """ Take in a checkbook object. Extracts only positive values into a list of dicts, with one dictionary
            representing one row.
        """
        self._data_list = []
        for row in all_transactions.get_data_list():
            if float(row['Amount']) > 0:
                self._data_list.append(row)
        # self.display()

    def display(self):
        """ Display the current data structure for testing purposes."""
        for row in self._data_list:
            print(row)

    def rename_columns(self):
        """ Renames column titles to their new names. Ignores columns to be deleted."""
        # Mapping of old keys to new keys
        key_mapping = {
            'Amount': 'Total Amount',
        }

        # go through every key value pair in every row and rename if needed... not very efficient :(
        for row_num in range(len(self._data_list)):
            # Uses dictionary comprehension
            new_row = {key_mapping.get(k, k): v for k, v in self._data_list[row_num].items()}
            self._data_list[row_num] = new_row

    def remove_unnecessary_columns(self):
        for row in self._data_list:
            del row['Check No']
            del row['Category']
            for i in range(1, 7):
                try:  # sometimes there are fewer than 6 apparently
                    del row['Split Category ' + str(i)]
                    del row['Split Amount ' + str(i)]
                    del row['Split Memo ' + str(i)]
                    del row['Split Class ' + str(i)]
                except KeyError:
                    break

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
            # move the value to the right of it into Third Party Payments. Same for F and G. This else statement
            # also handles a weird edge case where there is no letter anywhere in the row. This means it is actually
            # NOT a split payment and we need to look at the Payee information to decide if it should go in Copays
            # or Third Party Payments.
            else:
                is_blank_field_edge_case = True
                indexed_keys = list(row.keys())
                # Iterate with index
                for i in range(len(indexed_keys)):
                    key = indexed_keys[i]
                    if row[key] == 'D':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Copays'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'E':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Third Party Payments'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'F':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Refunds Received'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'G':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Transfers Received'] = split_amount
                        is_blank_field_edge_case = False

                if is_blank_field_edge_case:
                    if 'Terminal' in row['Payee']:
                        row['Copays'] = row['Amount']
                    else:
                        row['Third Party Payments'] = row['Amount']

    def check_total_amount_column(self):
        """
        This is not a strictly necessary function. I just included it to check to make sure
        the amounts in the category columns do in fact add up to the value in the Total Amount column.
        If there is a discrepancy, a warning message is printed to the console specifying the problem row.
        """
        for row_num in range(len(self._data_list)):
            row = self._data_list[row_num]
            supposed_total = float(row['Total Amount'])
            # All these try / except clauses are because '' throws a value error when you convert it to
            #   float. So I have to manually change it to zero.
            try:
                copays_amount = float(row['Copays'])
            except ValueError:
                copays_amount = 0
            try:
                third_party_payments_amount = float(row['Third Party Payments'])
            except ValueError:
                third_party_payments_amount = 0
            try:
                refunds_received_amount = float(row['Refunds Received'])
            except ValueError:
                refunds_received_amount = 0
            try:
                transfers_received_amount = float(row['Transfers Received'])
            except ValueError:
                transfers_received_amount = 0
            actual_total = (copays_amount +
                            third_party_payments_amount +
                            refunds_received_amount +
                            transfers_received_amount)
            if supposed_total != actual_total:
                # Add two below to account for index starting at 0 and also the fact that row 1 is occupied by
                #   column titles, not data.
                print("Error in row " + str(row_num + 2) + ": 'Total Amount' column differs from actual total of income categories.")


class Expenses:
    """
    MANY of the functions in here are going to be very similar to the ones in the Income class... the operations are very similar.
    My starting point was to literally copy the Income class over into the Expenses class, then modify.
    """

    def __init__(self, all_transactions):
        """ Take in a checkbook object. Extracts only negative values into a list of dicts, with one dictionary
            representing one row.
        """
        self._data_list = []
        for row in all_transactions.get_data_list():
            if float(row['Amount']) < 0:
                self._data_list.append(row)
        # self.display()

    def flip_to_positive(self) -> None:
        """ Flip all the negative values to positive."""
        for d in self._data_list:
            d['Amount'] = float(d['Amount']) * (-1)

    def display(self):
        """ Display the current data structure for testing purposes."""
        for row in self._data_list:
            print(row)

    def flip_columns(self, col1 : str, col2 : str) -> None:
        """
        Flips the order of two columns in the list of dicts.
        :param col1: string name of the first column.
        :param col2: string name of the second column.
        :return: Nothing, just reassign self._data_list to the newly created list of dicts.
        """
        new_list = []
        for d in self._data_list:
            new_dict = {}
            for k in d:
                if k == col1:
                    new_dict[col2] = d[col2]
                elif k == col2:
                    new_dict[col1] = d[col1]
                else:
                    new_dict[k] = d[k]
            new_list.append(new_dict)
        self._data_list = new_list

    def rename_columns(self):
        """ Renames column titles to their new names. Ignores columns to be deleted."""
        # Mapping of old keys to new keys
        key_mapping = {
            'Category': 'Officer\'s Comp (JJ)',
            'Split Category 1': 'Salaries and Wages',
            'Split Amount 1': 'Repairs and Maintenance',
            'Split Memo 1': 'Rent',
            'Split Class 1': 'Postage, Taxes, Licenses',
            'Split Category 2': 'Interest',
            'Split Amount 2': 'Depreciation',
            'Split Memo 2': 'Advertising, Employee Relations, Public Relations',
            'Split Class 2': 'Employee Benefits',
            'Split Category 3': 'Supplies, Medications',
            'Split Amount 3': 'Vaccines',
            'Split Memo 3': 'Services, Independent Contracts',
            'Split Class 3': 'Internet, Tel, Pagers',
            'Split Category 4': 'CC fees, Bank fees',
            'Split Amount 4': 'Subscriptions, Journals, Books, Ed Materials',
            'Split Memo 4': 'Professional Dues, Membership Fees',
            'Split Class 4': 'Insurance, Property',
            'Split Category 5': 'Travel, Convention',
            'Split Amount 5': 'Refunds paid out',
            'Split Memo 5': 'Transfers',
        }

        # go through every key value pair in every row and rename if needed... not very efficient :(
        for row_num in range(len(self._data_list)):
            # Uses dictionary comprehension
            new_row = {key_mapping.get(k, k): v for k, v in self._data_list[row_num].items()}
            self._data_list[row_num] = new_row

    def remove_unnecessary_columns(self):
        for row in self._data_list:
            try:
                del row['Split Class 5']
                del row['Split Category 6']
                del row['Split Amount 6']
                del row['Split Memo 6']
                del row['Split Class 6']
            except KeyError:
                break

    def write_to_csv(self):
        column_titles = self.get_column_titles()

        # name of csv file
        filename = "expenses.csv"

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
            # move the value to the right of it into Third Party Payments. Same for F and G. This else statement
            # also handles a weird edge case where there is no letter anywhere in the row. This means it is actually
            # NOT a split payment and we need to look at the Payee information to decide if it should go in Copays
            # or Third Party Payments.
            else:
                is_blank_field_edge_case = True
                indexed_keys = list(row.keys())
                # Iterate with index
                for i in range(len(indexed_keys)):
                    key = indexed_keys[i]
                    if row[key] == 'D':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Copays'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'E':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Third Party Payments'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'F':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Refunds Received'] = split_amount
                        is_blank_field_edge_case = False
                    elif row[key] == 'G':
                        next_key = indexed_keys[i + 1]
                        split_amount = row[next_key]
                        row['Transfers Received'] = split_amount
                        is_blank_field_edge_case = False

                if is_blank_field_edge_case:
                    if 'Terminal' in row['Payee']:
                        row['Copays'] = row['Amount']
                    else:
                        row['Third Party Payments'] = row['Amount']

    def check_total_amount_column(self):
        """
        This is not a strictly necessary function. I just included it to check to make sure
        the amounts in the category columns do in fact add up to the value in the Total Amount column.
        If there is a discrepancy, a warning message is printed to the console specifying the problem row.
        """
        for row_num in range(len(self._data_list)):
            row = self._data_list[row_num]
            supposed_total = float(row['Total Amount'])
            # All these try / except clauses are because '' throws a value error when you convert it to
            #   float. So I have to manually change it to zero.
            try:
                copays_amount = float(row['Copays'])
            except ValueError:
                copays_amount = 0
            try:
                third_party_payments_amount = float(row['Third Party Payments'])
            except ValueError:
                third_party_payments_amount = 0
            try:
                refunds_received_amount = float(row['Refunds Received'])
            except ValueError:
                refunds_received_amount = 0
            try:
                transfers_received_amount = float(row['Transfers Received'])
            except ValueError:
                transfers_received_amount = 0
            actual_total = (copays_amount +
                            third_party_payments_amount +
                            refunds_received_amount +
                            transfers_received_amount)
            if supposed_total != actual_total:
                # Add two below to account for index starting at 0 and also the fact that row 1 is occupied by
                #   column titles, not data.
                print("Error in row " + str(row_num + 2) + ": 'Total Amount' column differs from actual total of income categories.")




def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


class InitialCheckbook:
    """ Reads file into python data object, does initial data manipulation """

    def __init__(self, input_file):
        """
        Opens input data file, reads it into a list of dicts where each dict is a row
            and the keys are the column headers.
        """

        with open(input_file, mode='r', newline='', encoding='utf-8-sig') as input_file:
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

    def add_zeros(self):
        for row_num in range(len(self._data_list)):
            for key, val in self._data_list[row_num].items():
                if is_number(val):
                    if '.' not in val:
                        self._data_list[row_num][key] = val + '.00'
                    elif val[-2] == '.':
                        self._data_list[row_num][key] = val + '0'


def main():
    input_file = input("What file would you like to process?\nMake sure it is located in the same folder as this "
                       "script.\nSpell it perfectly with correct capitalization and "
                       "include .csv at the end\n")
    # open up csv file, store in a list of dicts
    transactions = InitialCheckbook(input_file)
    # add decimal points and zeros onto all numbers, so we don't have weird dollar amounts like '25' or '43.2'
    transactions.add_zeros()
    # reformat dates into integers, this is required for both income and expenses
    transactions.dates_to_day_numbers()
    # split data into income and expenses (expenses farther down)
    income = Income(transactions)
    # take care of columns D, E, F, and G based on adjacent letter. makes new columns at the end.
    income.categorize_payments()
    income.rename_columns()
    income.remove_unnecessary_columns()
    income.check_total_amount_column()
    # Write to csv
    income.write_to_csv()

    expenses = Expenses(transactions)
    expenses.flip_to_positive()
    # expenses.categorize_payments()
    expenses.flip_columns("Check No", "Payee")
    expenses.rename_columns()
    expenses.remove_unnecessary_columns()
    # expenses.check_total_amount_column() probably delete this
    expenses.write_to_csv()

    """
    income remaining tasks:
        go back through and add docstrings and comments...
        try to break it in a bunch of different ways? or just give it to mom with a warning on its robustness and assume later tweaks are needed.
            wrong file name
            ... brainstorm
        
    expenses:
        reorder / rename / add headers
        make amounts positive
    """


if __name__ == "__main__":
    main()
