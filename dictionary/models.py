from django.db import models


# Create your models here.
class Word(models.Model):
    # original text
    word = models.CharField(max_length=20)
    # language of the original text
    language = models.CharField(max_length=10)
    # english translation
    translation = models.CharField(max_length=20)

    def __unicode__(self):
    	return self.word