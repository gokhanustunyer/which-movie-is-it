from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100000)
    url = models.CharField(max_length=100000)
    image = models.CharField(max_length=100000)
    description = models.CharField(max_length=100000)
    review = models.CharField(max_length=100000)
    aggregateRating = models.CharField(max_length=100000)
    contentRating = models.CharField(max_length=100000)
    datePublished = models.CharField(max_length=100000)
    keywords = models.CharField(max_length=100000)
    actor = models.CharField(max_length=100000)
    director = models.CharField(max_length=100000)
    creator = models.CharField(max_length=100000)

    def __str__(self):
        return '{} | {}'.format(self.id,self.name)

class WOV(models.Model):
    name = models.CharField(max_length=100000)
    value = models.FloatField()

    def __str__(self):
        return '{} -- {}'.format(self.name,self.value)