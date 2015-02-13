# -*- coding: utf-8 -*-
from django import forms


class DataUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Upload new Dataset for Analysis!'
    )
    question = forms.CharField(
        label='What is your Question')
    answer = forms.CharField(
        label='What are the options')
