import os
from datetime import datetime

"""
Class Menu is implemented methods which allow to manage requests from users and show elements of menu
Methods:
    :header          - show menu of application
    :press_enter     - show text Press enter in the end of execution of request
    :clear           - clear screen
    :set_input       - extended version of input with messages, notes and applying validation rules
    :search_records  - return dictionary of records based on search criteria
    :loop_search     - recursively return records with ability to choose particular record or field 
    :field_value     - return value of specified field (without field name)
"""


class Menu:

    def __init__(self) -> None:
        self.get_search = []
        self.check = Validate()

    @staticmethod
    def header() -> None:
        print("[1]: Show balance \n" +
              "[2]: Add new record \n" +
              "[3]: Change record \n" +
              "[4]: Search")

    @staticmethod
    def press_enter() -> str:
        return input('Please press Enter to continue...')

    @staticmethod
    def clear() -> int:
        return os.system('cls' if os.name == 'nt' else 'clear')

    def set_input(self, message: str, note: str, validation_rule: str, **kwargs) -> str:
        # getting validate method by string representation
        valid = getattr(self.check, validation_rule)
        value = input(message)

        while not valid(value, **kwargs):
            value = input(note)

        return value

    @staticmethod
    def search_records(search_query: str, data: list) -> dict:

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
            self,
            message="Choose position of records for changing: ",
            note=f"The position is incorrect. Position should be a number between {keys[0]} and {keys[-1]} "
                 f"(see list above): ",
            validation_rule="is_valid_position",
            keys=keys
        ))
        self.get_search.append(position)
        return self.loop_search(data[position])

    @staticmethod
    def field_value(field: str) -> str:
        return field.split(':')[1].strip()


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
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_category(category: str) -> bool:
        if category in ["1", "2"]:
            return True
        return False

    @staticmethod
    def is_valid_amount(amount: str) -> bool:
        try:
            amount = float(amount)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_description(description: str) -> bool:
        if len(description) <= 256:
            return True
        return False

    @staticmethod
    def is_valid_position(position: str, **kwargs) -> bool:
        try:
            position = int(position)
            if position not in kwargs['keys']:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def is_search_field_empty(field: str) -> bool:
        if len(field) == 0:
            return False
        else:
            return True
