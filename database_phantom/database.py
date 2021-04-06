from copy import deepcopy
import json


class Database:
    def __init__(self):
        self.columns = []
        self.table = []

    def create_table(self, columns):
        self.columns = columns
        self.table = []

    def load_from_file(self, fileName):
        with open(fileName) as f:
            data = json.load(f)
            self.columns = data['columns']
            self.table = data['table']

    def save_into_file(self, fileName):
        with open(fileName, 'w') as f:
            json.dump({
                'columns': self.columns,
                'table': self.table
            }, f)

    def insert(self, new_row):
        new_row = deepcopy(new_row)
        for key in self.columns:
            if key not in new_row:
                new_row[key] = None
        self.table.append(new_row)

    def insert_where_col_equals(self, new_row, col, val):
        new_row = deepcopy(new_row)
        for row in self.table:
            if row[col] == val:
                for key in new_row:
                    row[key] = new_row[key]

    def select_all(self):
        return deepcopy(self.table)

    def select_where_col_equals(self, col, val):
        return deepcopy(list(row for row in self.table if row[col] == val))

    def select_where_col_in_list(self, col, vals):
        res = []
        for val in vals:
            res.extend(self.select_where_col_equals(col, val))
        return res
