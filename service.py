from datetime import datetime


class Menu:

    def __init__(self) -> None:
        self.check = Validate()

    def set_input(self, message, note, validation_rule):
        valid = getattr(self.check, validation_rule)
        value = input(message)

        while not valid(value):
            value = input(message)

        return value

    @staticmethod
    def search_records(search_query: str, data):

        search_results = {}
        start = 0
        for i, row in enumerate(data):
            if search_query in row:
                if row.startswith("date"):
                    start = i
                elif row.startswith("category"):
                    start = i - 1
                elif row.startswith("amount"):
                    start = i - 2
                elif row.startswith("description"):
                    start = i - 3

                search_results[start] = data[start:start + 4]

        return search_results

    # def choose_search_results(self, serach_results):

    #     if len(serach_results.items()) > 1:
    #         for i, record in serach_results.items():
    #             print(f'{i}) ', record)
    #         position = int(input("Choose position of records for changing: "))
    #     else:
    #         position = next(iter(serach_results))

    #     for i, row in enumerate(serach_results[position]):
    #         print(f'{i}) ', row)

    #     p = int(input("Choose position for changing [0, 1, 2 or 3]: "))
    #     old_value = serach_results[position][p].split(':')[1].strip()

    def loop_search(self, data: enumerate):

        for i, record in data:
            print(f'{i}) ', record)

        position = int(self.set_input(
            message="Choose position of records for changing: ",
            note="The position is incorrect. Position should be integer.",
            validation_rule="is_valid_position"))

        if isinstance(data[position], (dict, list)):
            self.loop_search(enumerate(data[position]))
        else:
            return data[position].split(':')[1].strip()


class Validate:

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_valid_date(date: str):
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_category(self, category: str):
        if category in ["1", "2"]:
            return True
        return False

    @staticmethod
    def is_valid_amount(self, amount: str):
        try:
            amount = float(amount)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_description(self, description: str):
        if len(description) <= 256:
            return True
        return False

    @staticmethod
    def is_valid_position(self, position: int):
        try:
            position = int(position)
            return True
        except ValueError:
            return False
