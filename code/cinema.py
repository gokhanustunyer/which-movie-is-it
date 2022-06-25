class Cinema:
    
    def __init__ (self,args):

        try:self.name = args['name']
        except:pass
        try:self.url = args['url']
        except:pass
        try:self.image = args['image']
        except:pass
        try:self.description = args['description']
        except:pass
        try:self.review = args['review']
        except:pass
        try:self.aggregateRating = args['aggregateRating']
        except:pass
        try:self.contentRating = args['contentRating']
        except:pass
        try:self.datePublished = args['datePublished']
        except:pass
        try:self.keywords = args['keywords']
        except:pass
        try:self.actor = args['actor']
        except:pass
        try:self.director = args['director']
        except:pass
        try:self.creator = args['creator']
        except:pass


    def __str__(self):
        return 'Movie Name: {} | IMDB Rating: {} | Lead Role: {} | Categories: {}'.format(
        self.name,self.rating,self.actors[0],self.categories)