import os
import json
from prettytable import PrettyTable

class DB:
    def __init__(self, name, path='.'):
        self._name = name.lower()
        self._path = os.path.join(path, self._name)
        self._tables = []
        self._format_name = '{}.json'

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def load_table(self, name):
        filepath = self._get_table_path(name)
        try:
            with open(filepath) as file:
                table_dict = json.load(file)
                if table_dict:
                    return self.make_table(name, table_dict)
        except Exception:
            print(f'Unable to open table {name!r}')

    def list_tables(self):
        return ''.join(self._format_name.format(table.name) for table in self._tables)

    def write_table(self, table):
        filepath = self._get_table_path(table.name)

        with open(filepath, 'w') as file:
            json.dump(table.columns, file, ensure_ascii=False, indent=4)
            print(f'Table {table.name} have been created successfully')
        self._tables.append(table)

    def delete_table(self, name):
        table  = self._find_table(name)
        if table:
            os.remove(self._get_table_path(name))
            self._tables.remove(table[0])
            print(f'Table {name} have been deleted successfully')
        else:
            print(f'Table {name!r} not found!')

    def make_table(self, name, table_dict):
        columns = list(table_dict.keys())
        table = Table(name, columns)
        for row in zip(*table_dict.values()):
            table.add(**dict(zip(columns, row)))
        return table

    def __str__(self):
        return '\n\n'.join(table.__str__() for table in self._tables)

    # HELPER METHODS
    def _find_table(self, name):
        return list(filter(lambda t: t.name == name, self._tables))

    def _get_table_path(self, name):
        filename = self._format_name.format(name)
        filepath = os.path.join(self.path, filename)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        return filepath


class Table:
    def __init__(self, name, columns):
        self.__id = 0
        self._name = name
        self._columns = {'id': [], **{arg: [] for arg in columns}}

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    def add(self, **kwargs):
        self.__id += 1
        kwargs['id'] = self.__id
        for col in self._columns:
            if col in kwargs:
                self._columns[col].append(kwargs[col])
            else:
                self._columns[col].append(None)

    def remove_where(self, key, value):
        if key in self._columns:
            try:
                index = self._columns[key].index(value)
                for column in self._columns:
                    self._columns[column].pop(index)
            except IndexError:
                print(f'Missing {value=} in {key}')

    def update_where(self, key, value, new_value):
        if key in self._columns:
            try:
                index = self._columns[key].index(value)
                self._columns[key][index] = new_value
            except IndexError:
                print(f'Missing {value=} in {key}')

    def __str__(self):
        x = PrettyTable()
        x.field_names = list(self._columns)
        x.add_rows(list(zip(*self._columns.values())))
        return x.__str__()

if __name__ == '__main__':
    p = os.path.dirname(__file__)
    db = DB('user_db', p)
    users = ({'name': 'paul', 'is_admin': False}, {'name': 'jhon', 'is_admin': False}, {'name': 'lisa', 'is_admin': False})
    table1 = Table('user', ('name', 'name', 'is_admin'))
    for user in users:
        table1.add(**user)
    print(table1)
    table1.remove_where('name', 'paul')
    print(table1)
    table1.update_where('name', 'lisa', 'elis')
    print(table1)
    db.write_table(table1)
    input('.........')
    table = db.load_table('user')
    print(table)
    print(db.list_tables())




