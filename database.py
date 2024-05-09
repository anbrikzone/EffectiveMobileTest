import json
import os
from pathlib import Path


class Database:

    def __init__(self, db_name=None) -> None:
        if db_name is None:
            db_name = "db.txt"
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connect()

    def connect(self) -> bool:
        db = Path(self.db_path)
        if not db.is_file():
            open(self.db_path, 'a').close()
        return True

    def read(self, mode='read') -> list:
        with open(self.db_path, 'r', encoding='utf-8') as file:
            if mode == 'read':
                return [x.strip() for x in file.readlines()]
            elif mode == 'write':
                return file.readlines()
            else:
                return [x.strip() for x in file.readlines()]

    def update(self, position, data):
        records = self.read(mode='write')
        records[position] = data + '\n'
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.writelines(records)

    def create(self, data) -> bool:
        try:
            with open(self.db_path, 'a', encoding='utf-8') as file:
                file.writelines([f'{key}: {value}\n' for key, value in data.items()])
                file.write('\n')
        except Exception as e:
            print(f"Something went wrong: {e}")

        return True
