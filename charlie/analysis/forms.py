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
