from code.lcm import encode,tuple_dict
import sqlite3

import os

BASE_DIR = os.getcwd()

class Searcher:

    limit = 30
    connect = sqlite3.connect(os.path.join(BASE_DIR,'db.sqlite3'),check_same_thread=False)
    cursor = connect.cursor()

    def __init__(self):
        self.similars = []


    def start(self,items:list):
        for item in items:
            self.find(item.lower())

        self.similars.sort(reverse=True)
        return self.similars

    def find(self,item):
        query = "SELECT id,name,description,keywords FROM wmovie_movie"
        Searcher.cursor.execute(query)
        datas = Searcher.cursor.fetchall()

        for data in datas:
            _id = data[0]
            data = self.editSummary(encode(data))
            if item in data :
                same = False
                value = self.getOtherInfos(_id)
                sim = self.calculateSim(item,data)
                for i in range(len(self.similars)):
                    if value == self.similars[i][1]:
                        self.similars[i][0] += sim
                        same = True
                if not same : self.similars.append([sim,value])

        

    def getOtherInfos(self,_id):
        query = "SELECT * FROM wmovie_movie where id = '{}'".format(_id)
        Searcher.cursor.execute(query)
        return Searcher.cursor.fetchall()


    def calculateSim(self,item,data):
        count = list(data).count(item)
        wov = self.query(item)

        return count*float(wov)

    def query(self,item):
        que = "select value from wmovie_wov where name = '{}'".format(item)
        Searcher.cursor.execute(que)
        return Searcher.cursor.fetchone()[0]

    def editSummary(self,data):
        return data.lower().split()

        
def main():
    s1 = Searcher()
    s1.start(['viking' ,'raid' ,'england' ,'ragnar'])

if __name__ == '__main__':
    main()