import os
import json
from prettytable import PrettyTable

class DB:
    def __init__(self, name, path='.'):
        self._name = f'{name}_db'
        self._cwd = os.path.join(path, self.name)
        self._tables = {}

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._cwd

    @property
    def tables(self):
        return self._tables

    def setup(self):
        try:
            os.mkdir(self._cwd)
        except:
            print(f'{self.name!r} already exists. Loading tables...')
            self.load()

    def load(self):
        files = os.listdir(self._cwd)
        for file in files:
            name = file.partition('.')[0]
            self.load_table(name)

    def load_table(self, name):
        try:
            with open(os.path.join(self._cwd, f'{name}.json')) as f:
                data = json.load(f)
            table = Table(name, list(data.keys())[1:])
            table.add_rows(*list(zip(*list(data.values())[1:])))
            self._tables[name] = table
        except Exception as e:
            print(e)

    def save(self):
        for table in self.tables.values():
            with open(os.path.join(self._cwd, f'{table.name}.json'), 'w') as file:
                rows = [list(row_dict.values()) for row_dict in table.data.values()]
                json.dump(dict(zip(table.columns, list(zip(*rows)))), file, indent=4, ensure_ascii=False)

    def append_table(self, table):
        self._tables[table.name] = table

    def find(self, name):
        return self.tables.get(name, None)

    def delete_table(self, name):
        removed = self._tables.pop(name, None)
        if removed:
            os.remove(os.path.join(self._cwd, f'{table.name}.json'))
            print(f'Table: {name!r} removed successfully.')
        else:
            print(f'Table: {name!r} not found. No table removed.')

    def __str__(self):
        return '\n\n'.join(table.__str__() for table in self.tables.values())


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

    def find_where(self, column_name, value):
        try:
            return tuple(filter(lambda row: row[column_name] == value, self.data.values()))[0]
        except Exception:
            return None

    def get_id_by(self, column_name, value):
        try:
            return self.find_where(column_name, value)['id']
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
            id = self.find_where(column_name, value)[0]['id']
            self.delete_by_id(id)
        except Exception as e:
            print(f'Value: {value} not found. No record removed.')

    def delete_all_where(self, column_name, value):
        rows = self.find_where(column_name, value)
        for row in rows:
            self.delete_by_id(row['id'])

    def update_by_id(self, id, column_name, new_value):
        try:
            self.data[id][column_name] = new_value
        except Exception as e:
            print(f'{id=} or {column_name=} not found. No record updated.')

    def update_where(self, column_name, value, new_value):
        try:
            id = self.find_where(column_name, value)[0]['id']
            self.update_by_id(id, column_name, new_value)
        except Exception as e:
            print(f'{column_name!r} not found. No record updated.')

    def update_all_where(self, column_name, value, new_value):
        rows = self.find_where(column_name, value)
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
    db = DB('app_testing', p)
    db.setup()
    print(db)
    users = (('paul', False), ('jhon', False), ('lisa', False))
    table = Table('user', ('name', 'is_admin'))
    for user in users:
        table.add_row(user)
    colors = (('red', True), ('blue', True), ('magenta', False))
    table_color = Table('color', ('color', 'primary'))
    for color in colors:
        table_color.add_row(color)
    # print(table)
    # print(table.data)
    # input()
    # table.update_all_where('name', 'jhon', 'felix')
    # table.update_all_where('name1', 'jhon', 'felix')
    # table.update_all_where('name', 'rex', 'felix')
    # table.update_by_id(3, 'is_admin', True)
    # table.update_by_id(8, 'is_admin', True)
    # table.update_where('name', 'paul', 'rosa')
    # print(table)
    # table.delete_all_where('name', 'lisa')
    # table.delete_all_where('name', 'lisa')
    # table.delete_all_where('name1', 'lisa')
    # table.delete_where('name', 'rosa')
    # table.delete_where('name', 'rosa')
    # table.delete_where('name1', 'rosa')
    # table.delete_by_id(2)
    # table.delete_by_id(2)
    # print('All lisa:', table.find_where('name', 'lisa'))
    # print('lisa:', table.get_id_by('name', 'lisa'))
    # print(table)
    input()
    db.append_table(table)
    db.append_table(table_color)
    print(db)
    db.save()
    new_db = DB('app', p)
    new_db.setup()
    table = db.find('user')
    users = (('felix', False), ('jess', False), ('rita', False))
    for user in users:
        table.add_row(user)

    print(table)
    db.save()





