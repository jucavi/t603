import os
import json
from prettytable import PrettyTable

class DB:
    def __init__(self, name, path='.'):
        self._name = name
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
        return table

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
        self._columns = ('id', *columns)
        self.data = {}

    @property
    def name(self):
        return self._name

    @property
    def columns(self):
        return self._columns

    def add_row(self, row):
        self.__id += 1
        row = (self.__id, *row)
        if len(row) != len(self._columns):
            raise ValueError('Invalid data!')
        self.data[self.__id] = dict(zip(self._columns, row))

    def add_rows(self, *rows):
        for row in rows:
            self.add_row(row)

    def find_by_id(self, id):
        return self.data[id]

    def find_all_by(self, column_name, value):
        try:
            return tuple(filter(lambda row: row[column_name] == value, self.data.values()))
        except Exception:
            return tuple()

    def get_id_by(self, column_name, value):
        try:
            return self.find_all_by(self, column_name, value)[0]['id']
        except:
            return None

    def delete_by_id(self, id):
        removed = self.data.pop(id, None)
        if removed:
            print(f'Id: {id} removed successfully.')
        else:
            print(f'Id: {id} not found. No record removed.')

    def delete_where(self, column_name, value):
        try:
            id = self.find_all_by(column_name, value)[0]['id']
            self.delete_by_id(id)
        except Exception as e:
            print(f'Value: {value} not found. No record removed.')

    def delete_all_where(self, column_name, value):
        rows = self.find_all_by(column_name, value)
        for row in rows:
            self.delete_by_id(row['id'])

    def update_by_id(self, id, column_name, new_value):
        try:
            self.data[id][column_name] = new_value
        except Exception as e:
            print(f'{id=} or {column_name=} not found. No record updated.')

    def update_where(self, column_name, value, new_value):
        try:
            id = self.find_all_by(column_name, value)[0]['id']
            self.update_by_id(id, column_name, new_value)
        except Exception as e:
            print(f'{column_name!r} not found. No record updated.')

    def update_all_where(self, column_name, value, new_value):
        rows = self.find_all_by(column_name, value)
        for row in rows:
            row[column_name] = new_value

    def __str__(self):
        x = PrettyTable()
        x.field_names = list(self._columns)
        for row in self.data.values():
            x.add_row(row.values())
        return x.__str__()

if __name__ == '__main__':
    p = os.path.dirname(__file__)
    db = DB('user_db', p)
    users = (('paul', False), ('jhon', False), ('lisa', False))
    table = Table('user', ('name', 'is_admin'))
    for user in users:
        table.add_row(user)
    print(table)
    table.update_all_where('name', 'jhon', 'felix')
    table.update_all_where('name1', 'jhon', 'felix')
    table.update_all_where('name', 'rex', 'felix')
    table.update_by_id(3, 'is_admin', True)
    table.update_by_id(8, 'is_admin', True)
    table.update_where('name', 'paul', 'rosa')
    print(table)
    table.delete_all_where('name', 'lisa')
    table.delete_all_where('name', 'lisa')
    table.delete_all_where('name1', 'lisa')
    table.delete_where('name', 'rosa')
    table.delete_where('name', 'rosa')
    table.delete_where('name1', 'rosa')
    table.delete_by_id(2)
    table.delete_by_id(2)
    print(table)







