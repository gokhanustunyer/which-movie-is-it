from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib.parse import urljoin
from cinema import Cinema


import json
import os
import shelve

from objtosql import SQLiteConverter

class IMDBScrapper:
    
    domain = 'https://www.imdb.com'

    def __init__(self):
        self.converter = SQLiteConverter('database/movies.db')
        self.indexed_links_db = shelve.open('database/iLinks/iLinks', writeback=True, flag='c')
    
    def scrap_single(self,url):
        req = urllib2.urlopen(url).read()
        source = BeautifulSoup(req,'html.parser')

        is_movie = IMDBScrapper.is_movie(source)

        if is_movie :       
            self.parse(source,url)
        else:
            return 'Movie is not founded'
        

    def scrapp_many(self,link):
        req = urllib2.urlopen(link).read()
        source = BeautifulSoup(req,'html.parser')

        tbody = source.find('tbody',{'class':'lister-list'}).find_all('tr')
        links = [item.find('a')['href'] for item in tbody]

        for link in links:
            if IMDBScrapper.domain+link in self.indexed_links_db: continue
            self.parse(IMDBScrapper.domain+link)


    @staticmethod
    def is_movie(source):
        if not isinstance(source, BeautifulSoup):
            return False
        
        try: 
            imdb_rating = source.find('div',{'class':'rating-bar__base-button'}).find('span').text
            actorsdiv = source.find('div',{'class':'title-cast__grid'}
            ).find_all('div')[1].find_all('div',{'data-testid':'title-cast-item'})
            actors = [actor.find('a')['aria-label'] for actor in actorsdiv]
        except:
            return False

        return True

    def parse(self,url):
        print('PAGE',url)

        req = urllib2.urlopen(url).read()
        source = BeautifulSoup(req,'html.parser')

        actorsdiv = source.find('div',{'class':'title-cast__grid'}
        ).find_all('div')[1].find_all('div',{'data-testid':'title-cast-item'})
        actors = [actor.find('a')['aria-label'] for actor in actorsdiv]

        cInfo = source.find('script',{'type':'application/ld+json'})
        jContent = json.loads(cInfo.text)
        jContent.pop('@context')

        _cinObj = Cinema(jContent)
    
        _cinObj.keywords = self.getKeywords(url)
        _cinObj.actor = actors


        self.converter.createTable('movies')
        column, values = self.converter.convert(_cinObj)
        self.converter.fillColumn(column,values)
        self.indexed_links_db[url] = None


        

    def getKeywords(self,url):
    
        kwPageR = urllib2.urlopen(urljoin(url,'keywords')).read()
        kwPage = BeautifulSoup(kwPageR, 'html.parser')

        kwDivs = kwPage.find_all('div',{'class':'sodatext'})
        keywords = [kw.text.strip().replace('-',' ') for kw in kwDivs]

        return keywords

def main():
    _scrapper = IMDBScrapper()
    _scrapper.scrapp_many('https://www.imdb.com/india/top-rated-indian-movies/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=470df400-70d9-4f35-bb05-8646a1195842&pf_rd_r=ZN3QA0TPTQA1EDKD5RCP&pf_rd_s=right-4&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_ql_7')

if __name__ == '__main__':
    main()