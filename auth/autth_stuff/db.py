import os
import json
from prettytable import PrettyTable

class DB:
    def __init__(self, name, path='.'):
        self._name = name.lower()
        self._path = path
        self._tables = []

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def load_table(self, name):
        try:
            with open(self._filepath(name)) as file:
                table_json = json.load(file)
        except Exception:
            print(f'Unable to open table {name!r}')

    def create_table(self, name, *args):
        name = name.lower()
        filename = f'{self.name}_{name}.json'
        filepath = self._filepath(filename)

        if os.path.exists(filepath):
            print(f'Table {name!r} already exists.')
            table = self.load_table(filename)
        else:
            table = Table(name, *args)
            with open(filepath, 'w') as file:
                json.dump(table.columns, file, ensure_ascii=False, indent=4)
                print(f'Table {name} have been created successfully')

        self._tables.append(table)
        return table

    def remove_table(self, name):
        table  = self._find_table(name)
        if table:
            os.remove(self._filepath(name))
            self._tables.remove(table[0])
            print(f'Table {name} have been deleted successfully')
        else:
            print(f'Table {name!r} not found!')

    def __contains__(self, name):
        return any(t.name == name for t in self._tables)

    def __str__(self):
        return '\n\n'.join(str(table) for table in self._tables)

    # HELPER METHODS
    def _find_table(self, name):
        return list(filter(lambda t: t.name == name, self._tables))

    def _filepath(self, filename):
        return os.path.join(self.path, filename)



class Table:
    def __init__(self, name, *columns):
        self._name = name
        self._columns = {arg: [] for arg in columns}

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    def add(self, row):
        for col in self._columns:
            if col in row:
                self._columns[col].append(row[col])
            else:
                self._columns[col].append(None)

    def remove(self, key, value):
        if key in self._columns:
            try:
                index = self._columns[key].index(value)
                for column in self._columns:
                    column.pop(index)
            except IndexError:
                print(f'Missing {value=} in {key}')

    def __str__(self):
        x = PrettyTable()
        x.field_names = list(self._columns)
        x.add_rows(list(zip(*self._columns.values())))
        return x.__str__()

if __name__ == '__main__':
    p = os.path.dirname(__file__)
    db = DB('test', p)
    user = {'id': 1, 'name': 'paul'}
    user = {'id': 2, 'name': 'jhon'}
    user = {'id': 3, 'name': 'lisa'}
    db.remove_table('users')
    print(db._tables)
    # t = Table('test', 'id', 'name')
    # ids = 1
    # names = 'jhon'
    # t.add({'id':ids, 'name':names})
    # print(t)
    # ary = [Table('yo'), Table('tu')]

    # print('yo' in ary)
