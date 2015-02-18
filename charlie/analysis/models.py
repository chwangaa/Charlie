from django.db import models
from django.contrib.auth.models import User


class DataSource(models.Model):
    docfile = models.FileField(upload_to='data/%Y/%m/%d')
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='owned_data')


class SMS(models.Model):
    country = models.CharField(max_length=20)
    rstation = models.CharField(max_length=20)
    # physical limit of SMS is 160 characters
    text = models.CharField(max_length=160)
    source = models.ForeignKey('DataSource')
    opinion = models.CharField(max_length=20)
    index = models.IntegerField()
    # derived fields
    modifield_text = models.CharField(max_length=160)
    language = models.CharField(max_length=20)


class Word(models.Model):
    # original text
    word = models.CharField(max_length=20)
    # language of the original text
    language = models.CharField(max_length=10)
    # english translation
    translation = models.CharField(max_length=20, null=True)

    word_type = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return self.word