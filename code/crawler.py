from objtosql import SQLiteConverter
from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib.parse import urljoin

from scrapper import IMDBScrapper
from cinema import Cinema
import json

import shelve


class Crawler:

    domain = 'https://www.imdb.com'
    
    def __init__(self):
        self.converter = SQLiteConverter('database/movies.db')

        self.crawling_db = shelve.open('database/iLinks/iLinks', writeback=True, flag='c')

    def crawl(self,pages:list,depth=3):
        for i in range(depth):
            print('depth {}'.format(i))
            newpages = []
            for page in pages:

                if page in self.crawling_db:continue

                if 'imdb' not in page : return 'Unexpected Domain'

                try : reading = urllib2.urlopen(page).read()
                except : continue
                content = BeautifulSoup(reading,'html.parser')


                self.wsOperations(content,page)
                self.add_page_to_db(page)

                links = content.find_all('a')
                for link in links:
                    if 'href' in link.attrs :
                        newpages.append(Crawler.domain+link['href'])

            pages = newpages



    def wsOperations(self,content,url):
        is_movie = IMDBScrapper.is_movie(content)

        if is_movie:
            _cinOBJ = self.parseMovie(content,url)
            self.converter.createTable('movies')
            column, values = self.converter.convert(_cinOBJ)
            self.converter.fillColumn(column,values)


    def add_page_to_db(self,domain):
        self.crawling_db[domain] = None


    def checkDomain(self,domain):
        if 'imdb' not in domain: return False
        if ',' in domain:return domain.split(',')[0]
        return True


    def parseMovie(self,source,url):

        actorsdiv = source.find('div',{'class':'title-cast__grid'}
        ).find_all('div')[1].find_all('div',{'data-testid':'title-cast-item'})
        actors = [actor.find('a')['aria-label'] for actor in actorsdiv]

        cInfo = source.find('script',{'type':'application/ld+json'})
        jContent = json.loads(cInfo.text)
        jContent.pop('@context')

        _cinOBJ = Cinema(jContent)
        
        _cinOBJ.keywords = self.getKeywords(url)
        _cinOBJ.actor = actors

        return _cinOBJ


    def getKeywords(self,url):
    
        kwPageR = urllib2.urlopen(urljoin(url,'keywords')).read()
        kwPage = BeautifulSoup(kwPageR, 'html.parser')

        kwDivs = kwPage.find_all('div',{'class':'sodatext'})
        keywords = [kw.text.strip().replace('-',' ') for kw in kwDivs]

        return keywords

def main():
    c1 = Crawler()

    c1.crawl(['https://www.imdb.com/title/tt5433138/?ref_=nv_sr_srsg_2'])


if __name__ == '__main__':
    main()