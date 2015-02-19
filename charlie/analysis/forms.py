# -*- coding: utf-8 -*-
from django import forms


class DataUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Upload a new dataset for analysis!'
    )
    question = forms.CharField(
        label='What is your question?')
    answer = forms.CharField(
        label='What are your options?')

    def is_valid(self):
        # TODO: check if all the necessary headings are there
        return True


class CreateWordForm(forms.Form):
    name = forms.CharField(
        label='Please enter the name')


class CreateDictForm(forms.Form):
    word = forms.CharField(
        label = 'Please enter the word')
    trans = forms.CharField(
        label = 'Please enter the translation')
    language = forms.CharField(
        label = 'Please enter the language')