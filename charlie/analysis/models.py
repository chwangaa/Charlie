from django.db import models
from django.contrib.auth.models import User


class DataSource(models.Model):
    docfile = models.FileField(upload_to='data/%Y/%m/%d')
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='owned_data')


class Category(models.Model):
    name = models.CharField(max_length=20)


class CategoryLabel(models.Model):
    label = models.CharField(max_length=20)
    category = models.ForeignKey('Category')


class SMS(models.Model):
    country = models.CharField(max_length=20)
    rstation = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    source = models.ForeignKey('DataSource')
    opinion = models.CharField(max_length=20)
    index = models.IntegerField()


class Word(models.Model):
    word = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    rstation = models.CharField(max_length=20)
    sms = models.ForeignKey(SMS, related_name='words')
