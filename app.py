import os
from database import Database
from service import Validate, Menu


class App:

    def __init__(self) -> None:
        self.db = Database()
        self.check = Validate()
        self.menu = Menu()

    def run(self):
        while True:
            self.header()
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

    @staticmethod
    def header():
        print("[1]: Show balance \n" +
              "[2]: Add new record \n" +
              "[3]: Change record \n" +
              "[4]: Search")

    def show_balance(self):
        income = 0
        expenses = 0

        all_records = self.db.read()
        for i, row in enumerate(all_records):
            if row.startswith('category'):
                amount = float(all_records[i + 1].split(":")[1].strip())
                if row.split(":")[1].strip() == "income":
                    income += amount
                else:
                    expenses += amount

        print(f"Balance:    {round(income - expenses, 1)}\n" +
              f"Income:     {income}\n" +
              f"Expenses:   {expenses}")
        input()
        return True

    def add_record(self):
        record = {
            'date': self.menu.set_input(
                message="Add date [dd.mm.yyyy]: ",
                note="The date is incorrect. Please follow suggested template - dd.mm.yyyy",
                validation_rule="is_valid_date"
            ), "category": self.menu.set_input(
                message="Choose category - [1] for income and [2] for expenses: ",
                note="The category is incorrect. Please choose suggested type - [1] for income and [2] for expenses:",
                validation_rule="is_valid_category"
            ), "amount": self.menu.set_input(
                message="Input amount of money [0 or .0]: ",
                note="The amount is incorrect. Please choose suggested type - 0 or .0:",
                validation_rule="is_valid_amount"
            ), "description": self.menu.set_input(
                message="Input description (max 256 symbols): ",
                note="The description is too long. 256 symbols are maximum.",
                validation_rule="is_valid_description"
            )}

        record['category'] = "income" if record['category'] == "1" else "expenses"

        if self.db.create(record):
            print('The record has been added.')
            return True
        else:
            return False

    def change_record(self):
        print(
            "You are going to change record. Please type date, category, amount or description to identify the record.")
        search_text = input('Search: ')
        results = self.menu.search_records(search_text, self.db.read())

        # if len(results.items()) > 1:
        #     for i, record in results.items():
        #         print(f'{i}) ', record)
        #     position = int(input("Choose position of records for changing: "))
        # else:
        #     position = next(iter(results))

        # for i, row in enumerate(results[position]):
        #     print(f'{i}) ', row)

        # p = int(input("Choose position for changing [0, 1, 2 or 3]: "))
        # old_value = results[position][p].split(':')[1].strip()
        old_value = self.menu.loop_search(results)
        message = f"Old value - {old_value}, New value: "

        match p:
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

        results[position][p] = results[position][p].replace(old_value, new_value)
        # print(position)
        self.db.update(position=position + p, data=results[position][p])
        # print(p)

    def remove_record(self):
        pass
