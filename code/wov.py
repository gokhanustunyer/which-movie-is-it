import sqlite3
import shelve

from lcm import encode,decode

class WOV:

    connect = sqlite3.connect('database/movies.db')
    cursor = connect.cursor()

    def __init__(self):
        self.db = shelve.open('database/WOV/wov', writeback=True, flag='c')

    def update(self):
        datas = self.getSQL()

        counter = {}
        for data in datas:
            if len(data) < 3:continue
            counter.setdefault(data,0)
            counter[data] += 1
        self.save(counter)

        self.read()

    def read(self,word):
        if word in self.db:print(self.db[word])
        else : return 'Word not founded'

    def getSQL(self):
        query = 'SELECT name,description,keywords FROM movies'
        WOV.cursor.execute(query)
        data = WOV.cursor.fetchall()
        data = self.editSummary(encode(data))
        
        return data


    def save(self,dct:dict):
        if type(dct) != dict:return 'Argument must be dict'
        for key,value in dct.items():
            self.db[key] = 1/int(value)

    def editSummary(self,data):
        return data.lower().split()



def main():
    w1 = WOV()
    while True:
        print('Update Database [0]')
        print('Check Word [1]')
        print('Exit [2]')
        choi = input('Choice: ')   

        if choi == '0' :
            sure = input('You sure about update db?[Y/n]:')
            if sure == 'Y':w1.update()

        elif choi == '1':
            word = input('Word: ')
            w1.read(word)

        elif choi == '2':
            break
                
if __name__ == '__main__':
    main()