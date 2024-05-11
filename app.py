import os
from database import Database
from service import Validate, Menu

"""
Class App is implemented main methods of program.
Methods:
    :run               - run application with menu
    :show_balance      - show balance (incomes and expenses)
    :add_record        - add record to database
    :change_record     - change record in database
    :search_record     - search record in database 
"""


class App:

    def __init__(self) -> None:
        self.db = Database()
        self.check = Validate()
        self.menu = Menu()

    def run(self) -> None:
        while True:
            self.menu.clear()
            self.menu.header()
            try:
                menu_item = int(input('Please select menu item [number]: '))
            except ValueError:
                menu_item = 0
            match menu_item:
                case 1:
                    self.show_balance()
                case 2:
                    self.add_record()
                case 3:
                    self.change_record()
                case 4:
                    self.search()

    def show_balance(self) -> str:
        income = 0
        expenses = 0

        all_records = self.db.read()
        for i, row in enumerate(all_records):
            if row.startswith('category'):
                # Get amount of money for category
                amount = float(self.menu.field_value(all_records[i + 1]))
                if self.menu.field_value(row) == "income":
                    income += amount
                else:
                    expenses += amount

        print(f"Balance:    {round(income - expenses, 2)}\n" +
              f"Income:     {round(income, 2)}\n" +
              f"Expenses:   {round(expenses, 2)}")
        return self.menu.press_enter()

    def add_record(self) -> str:
        # Obtain user's input and validate them
        record = {
            'date': self.menu.set_input(
                message="Add date [dd.mm.yyyy]: ",
                note="The date is incorrect. Please follow suggested template - dd.mm.yyyy",
                validation_rule="is_valid_date"
            ),
            "category": self.menu.set_input(
                message="Choose category - [1] for income and [2] for expenses: ",
                note="The category is incorrect. Please choose suggested type - [1] for income and [2] for expenses:",
                validation_rule="is_valid_category"
            ),
            "amount": self.menu.set_input(
                message="Input amount of money [0 or .0]: ",
                note="The amount is incorrect. Please choose suggested type - 0 or .0:",
                validation_rule="is_valid_amount"
            ),
            "description": self.menu.set_input(
                message="Input description (max 256 symbols): ",
                note="The description is too long. 256 symbols are maximum.",
                validation_rule="is_valid_description"
            )}
        # Convert numbers to text for categories
        record['category'] = "income" if record['category'] == "1" else "expenses"

        if self.db.create(record):
            print('The record has been added.')
        else:
            print('The record has not been created.')
        return self.menu.press_enter()

    def change_record(self):
        search_text = self.menu.set_input(
            message="You are going to change record. Please type date, category, amount or description to identify "
                    "the record.\n"
                    "Search: ",
            note="Please fill out search field.",
            validation_rule="is_search_field_empty"
        )
        results = self.menu.search_records(search_text, self.db.read())

        row_number, field_number = self.menu.loop_search(results)
        old_value = self.menu.field_value(results[row_number][field_number])
        new_value = ""
        message = f"Old value - {old_value}, New value: "

        match field_number:
            case 0:
                new_value = self.menu.set_input(
                    message=message,
                    note="The date is incorrect. Please follow suggested template - dd.mm.yyyy",
                    validation_rule="is_valid_date"
                )
            case 1:
                new_value = self.menu.set_input(
                    message=message,
                    note="The category is incorrect. Please choose suggested type - [1] for income and [2] for "
                         "expenses:",
                    validation_rule="is_valid_category"
                )
            case 2:
                new_value = self.menu.set_input(
                    message=message,
                    note="The amount is incorrect. Please choose suggested type - 0 or .0:",
                    validation_rule="is_valid_amount"
                )
            case 3:
                new_value = self.menu.set_input(
                    message=message,
                    note="The description is too long. 256 symbols are maximum.",
                    validation_rule="is_valid_description"
                )

        results[row_number] = results[row_number][field_number].replace(old_value, new_value)
        if self.db.update(position=(row_number + field_number), data=results[row_number]):
            print('Data has been updated.')
        else:
            print('Data not updated.')
        return self.menu.press_enter()

    def search(self):
        search_text = self.menu.set_input(
            message="Search: ",
            note="Please fill out search field.",
            validation_rule="is_search_field_empty"
        )
        results = self.menu.search_records(search_text, self.db.read())
        if len(results) > 1:
            for i, record in results.items():
                print(f'{i}) ', record)
        else:
            print(f'There is no records with search text "{search_text}".')
        self.menu.press_enter()
