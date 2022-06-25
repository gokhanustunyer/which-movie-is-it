from cinema import Cinema
from lcm import *
import sqlite3
import json


class SQLiteConverter:

    def __init__(self,db_name):
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()

    def createTable(self, tname):
        self.tname = tname
        try:
            self.cursor.execute('CREATE TABLE {} (id INTEGER PRIMARY KEY, name TEXT UNIQUE)'.format(self.tname))
        except sqlite3.OperationalError:
            return ('table already exists')

    def convert(self,obj):
        dct = {}
        for key,value in obj.__dict__.items():
            item, typ = SQLiteConverter.checkType(value)

            if typ == None :
                print('Unexpected data type')
                continue

            self.createColumn(key, typ)
            dct[key] = item

        columns = tuple(dct.keys())
        values = tuple(dct.values())   

        return columns, values

    def createColumn(self, c_name, typ):
        try:
            if c_name == 'name' : return
            self.cursor.execute('ALTER TABLE {} ADD COLUMN {} {}'.format(self.tname, c_name, typ))
            self.connect.commit()
        except sqlite3.OperationalError:
            return 'Column already created'


    def fillColumn(self, columns, values):
        query = 'INSERT INTO {} {} values{}'.format(self.tname, columns, values)
        try:self.cursor.execute(query)
        except sqlite3.IntegrityError: return 'movie already added'
        self.connect.commit()


    @staticmethod
    def checkType(item):
        if type(item) == str:return item,'TEXT'
        elif type(item) == dict:return json.dumps(item),'TEXT'
        elif type(item) == dict:return item,'INTEGER'
        elif type(item) == float:return item,'NUMERIC'
        elif type(item) == list:return encode(item),'TEXT'
        elif type(item) == tuple:return encode(item),'TEXT'
        elif type(item) == bool:return 1, 'TEXT' if item == True else 0, 'TEXT'
        else:return None, None

