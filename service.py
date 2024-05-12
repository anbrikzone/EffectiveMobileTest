import os
from datetime import datetime

"""
Class Menu is implemented methods which allow to manage requests from users and show elements of menu
Methods:
    :header          - show menu of application
    :press_enter     - show text Press enter in the end of execution of request
    :set_input       - extended version of input with messages, notes and applying validation rules
    :search_records  - return dictionary of records based on search criteria
    :loop_search     - recursively return records with ability to choose particular record or field 
"""


class Menu:

    def __init__(self) -> None:
        self.get_search = []
        # self.check = Validate()

    @staticmethod
    def header() -> None:
        """
        :return: menu of application
        """
        print("[1]: Show balance \n" +
              "[2]: Add new record \n" +
              "[3]: Change record \n" +
              "[4]: Search")

    @staticmethod
    def press_enter() -> str:
        """
        :return: text "Press enter..."
        """
        return input('Please press Enter to continue...')

    @staticmethod
    def set_input(message: str, note: str, validation_rule: str, **kwargs) -> str:
        """
        :param message: first message to display in input
        :param note: message if validation return false
        :param validation_rule: validation rule to use in input
        :param kwargs: additional arguments to pass to input function
        :return: value of specified field (without field name)
        """
        # getting validate method by string representation
        valid = getattr(Validate(), validation_rule)
        value = input(message)

        while not valid(value, **kwargs):
            value = input(note)

        return value

    @staticmethod
    def search_records(search_query: str, data: list) -> dict:
        """
        :param search_query: text which we want to find in database
        :param data: all records from database
        :return:
        """
        search_results = {}
        start = 0
        for i, row in enumerate(data):
            if search_query.lower() in row.lower():
                if row.startswith("date"):
                    start = i
                elif row.startswith("category"):
                    start = i - 1
                elif row.startswith("amount"):
                    start = i - 2
                elif row.startswith("description"):
                    start = i - 3
                # start:start + 4 - allow to obtain whole record with all fields: date, category, amount and description
                search_results[start] = data[start:start + 4]

        return search_results

    def loop_search(self, data: dict | list | str) -> list[int]:
        """
        :param data: set of data
        :return: list of numbers: position of record and field's numer
        """
        if isinstance(data, dict):
            # check how many records have been returned.
            # If more than one - show them all, if only one - show fields directly
            if len(data) > 1:
                for i, record in data.items():
                    print(f'{i}) ', record)
                keys = list(data.keys())
            else:
                self.get_search.append(next(iter(data)))
                return self.loop_search(data[next(iter(data))])
        elif isinstance(data, list):
            for i, record in enumerate(data):
                print(f'{i}) ', record)
            keys = list(range(len(data)))
        else:
            return self.get_search

        position = int(Menu.set_input(
            message="Choose position of records for changing: ",
            note=f"The position is incorrect. Position should be a number between {keys[0]} and {keys[-1]} "
                 f"(see list above): ",
            validation_rule="is_valid_position",
            keys=keys
        ))
        self.get_search.append(position)
        return self.loop_search(data[position])


"""
Class Utils - set of methods for processing values
Methods:
    :category_converter     - convert numbers 1 and 2 to text income and expenses
    :field_value            - return value of specified field (without field name)
    :date_converter         - convert date to to YYYY-MM-DD format
    :clear                  - clear console's screen
"""


class Utils:

    @staticmethod
    def category_converter(category_str: str) -> str:
        """
        :param category_str: number of category to be converted
        :return: category in text format
        """
        return "income" if category_str == "1" else "expenses"

    @staticmethod
    def field_value(field: str) -> str:
        """
        :param field: field with name and value
        :return: value of field (without field name)
        """
        return field.split(':')[1].strip()

    @staticmethod
    def date_converter(date_str: str) -> object:
        """
        :param date_str: date as string
        :return: date as datetime object in YYYY-MM-DD format
        """
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")

    @staticmethod
    def clear() -> int:
        """
        :return: clear console's screen
        """
        return os.system('cls' if os.name == 'nt' else 'clear')


"""
Class Validate allow to validate input from user
Methods:
    :is_valid_date          - The dates in format dd.mm.yyyy only is allowed
    :is_valid_category      - Only 1 and 2 categories are allowed. Using numbers is convenient for input
    :is_valid_amount        - Amount as integer or float only is allowed
    :is_valid_description   - Description with maximum length in 256 symbols is allowed
    :is_valid_position      - Row position in database in integer format is allowed, between range of presented list
    :is_search_field_empty  - Search field shouldn't be empty
"""


class Validate:

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_valid_date(date: str) -> bool:
        """
        :param date: date as string
        :return: True if date is valid, False otherwise
        """
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_category(category: str) -> bool:
        """
        :param category: category numbers in string type (get directly from input)
        :return: True if number of category present in the list, False otherwise
        """
        if category in ["1", "2"]:
            return True
        return False

    @staticmethod
    def is_valid_amount(amount: str) -> bool:
        """
        :param amount: amount of money to be validated
        :return: True if amount is valid, False otherwise
        """
        try:
            amount = float(amount)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_description(description: str) -> bool:
        """
        :param description: text of description
        :return: True if description is less 256 symbols, False otherwise
        """
        if len(description) <= 256:
            return True
        return False

    @staticmethod
    def is_valid_position(position: str, **kwargs) -> bool:
        """
        :param position: number in string type (get directly from input)
        :param kwargs: optional arguments to pass list of allowed keys
        :return: true if position is in the keys list, False otherwise
        """
        try:
            position = int(position)
            if position not in kwargs['keys']:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def is_search_field_empty(value: str) -> bool:
        """
        :param value: value for searching
        :return: true if value is not empty, False otherwise
        """
        if len(value) == 0:
            return False
        else:
            return True
