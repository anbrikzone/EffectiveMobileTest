import os
from pathlib import Path
from typing import Type

"""
Class Database allow read/write data into file database
Methods:
    :connect    - create file of database if it doesn't exist'
    :read       - read from database file with 2 modes: read (without \n) and write (all characters) 
    :update     - update row in database file
    :create     - create a new records in database file in key:value format
"""


class Database:

    def __init__(self, db_name: Type[None | str] = None) -> None:
        if db_name is None:
            db_name = "db.txt"
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connect()

    def connect(self) -> bool:
        """
        :return: True if database exists, else False
        """
        db = Path(self.db_path)
        if not db.is_file():
            try:
                open(self.db_path, 'a').close()
            except PermissionError:
                return False
        return True

    def read(self, mode: str = 'read') -> list:
        """
        :param mode: read or write: read - without \n, write - all characters
        :return: list of rows from database file
        """
        with open(self.db_path, 'r', encoding='utf-8') as file:
            if mode == 'read':
                return [x.strip() for x in file.readlines()]
            elif mode == 'write':
                return file.readlines()
            else:
                return [x.strip() for x in file.readlines()]

    def update(self, position: int, data: str) -> bool:
        """
        :param position: row number to update
        :param data: string to update
        :return: True if data was updated, else False
        """
        records = self.read(mode='write')
        records[position] = data + '\n'
        try:
            with open(self.db_path, 'w', encoding='utf-8') as file:
                file.writelines(records)
            return True
        except (FileNotFoundError, PermissionError):
            return False

    def create(self, data: dict) -> bool:
        """
        :param data: Dictionary to create
        :return: True if data was created, else False
        """
        with open(self.db_path, 'a', encoding='utf-8') as file:
            file.writelines([f'{key}: {value}\n' for key, value in data.items()])
            file.write('\n')

        return True
