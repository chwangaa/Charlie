# -*- coding: utf-8 -*-
from django import forms


class DataUploadForm(forms.Form):
    docfile = forms.FileField(
        label='Upload your dataset for analysis'
    )
    question = forms.CharField(
        label='What is your question?')
    opinions = forms.CharField(
        label='What opinions are you interested at?')

    def clean_opinions(self):
        opinions = self.cleaned_data['opinions']
        opinions = opinions.replace(" ", "")
        # all the possible group of opinions
        groups = opinions.split(';')
        try:
            cleaned_opinions = {}
            for group in groups:
                name = group.split(':')[0]
                options = group.split(':')[1].split(',')
                for option in options:
                    option = option.lower()
                    cleaned_opinions[option] = name
            return cleaned_opinions
        except Exception:
            raise forms.ValidationError(
                        "ERROR: \
                        please enter a valid opinion list with the format:\
                        LABEL1: OP11, OP12; LABEL2: OP21, OP22\
                        e.g. AIDS: aids, sida; MALARIA: malaria, maleria")

    def clean_docfile(self):
        docfile = self.cleaned_data['docfile']
        import csv
        reader = csv.reader(docfile)
        labels = reader.next()
        if 'SMS' not in labels:
            raise forms.ValidationError(
                        "ERROR: \
                        the file does not have a SMS column")
        if 'Country' not in labels:
            raise forms.ValidationError(
                        "ERROR: \
                        the file does not have a Country column")
        return docfile


class CreateWordForm(forms.Form):
    name = forms.CharField(
        label='Please enter the name')


class CreateDictForm(forms.Form):
    word = forms.CharField(
        label='Please enter the word')
    trans = forms.CharField(
        label='Please enter the translation')
    language = forms.CharField(
        label='Please enter the language')
