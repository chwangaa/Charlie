# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template.loader import render_to_string
from models import DataSource, Word
from forms import DataUploadForm, CreateNameForm, CreateDictForm, \
                  CreateSkipForm, CreateTypoForm
from utils import initializeDatabaseForDataSource, getCount,\
                  renderOpinion, getDataSourceOpinions, getFrequencyList
from django.db.models import Q
import json


@login_required
def dashboard(request):
    # Handle file upload
    if request.method == 'POST':
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            question = data['question']
            answers_raw = data['opinions']
            opinions = renderOpinion(answers_raw)
            newdoc = DataSource(
                docfile=request.FILES['docfile'], name=question,
                owner=request.user, opinions=opinions)
            newdoc.save()

            initializeDatabaseForDataSource(newdoc, answers_raw)
            source_id = newdoc.id
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('analysis', args=[source_id]))
        else:
            return render_to_response(
                'dashboard.html',
                {'form': form, 'name': request.user.username},
                context_instance=RequestContext(request))
    else:
        form = DataUploadForm()  # A empty, unbound form

    # Load documents for the list page
    documents = DataSource.objects.all().filter(owner=request.user)

    # Render list page with the documents and the form
    return render_to_response(
        'dashboard.html',
        {'documents': documents, 'form': form, 'name': request.user.username},
        context_instance=RequestContext(request)
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('landing'))
    # Redirect to a success page.


@login_required
def analysis(request, datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    sms_set = source.sms_set.all()

    # get the sms_set
    data = []
    # use texts to concat all the messages
    for d in sms_set:
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'SMS': d.text,
                    'opinion': d.opinion,
                    'modified_text': d.modifield_text,
                    'Index': d.index,
                    'Language':d.language
                    }
        data.append(instance)

    # get data for text_display_view
    opinions = getDataSourceOpinions(datasource_id)
    table = render_to_string("table.html",
                             {"data": data, "opinions": opinions})

    # get data for word_cloud_view
    word_freq = json.dumps(getFrequencyList(datasource_id))

    # get pie_chart
    data_js = json.dumps(data)
    opinions = sms_set.values_list('opinion', flat=True)
    data = getCount(opinions)
    title = "Overview of Opinions Regarding: " + source.name
    pie_chart_data = {"data": data, "title": title}
    pie_chart = render_to_string("pie_chart.html", pie_chart_data)

    # get column_chart
    from utils import getOpinionCountryBreakDown
    breakdown = getOpinionCountryBreakDown(datasource_id)
    title = "Country Break Down Regarding: " + source.name
    countries = breakdown[0]
    data_list = breakdown[1:]
    column_chart_data = {"data": data_list,
                         "title": title,
                         "countries": countries}
    column_chart = render_to_string("column_chart.html", column_chart_data)

    # get the country list and rstation list for sidebar
    countries = sms_set.values_list('country', flat=True).distinct()
    countries = [str(e) for e in countries]
    rstations = sms_set.values_list('rstation', flat=True).distinct()
    rstations = [str(e) for e in rstations]
    opinions = getDataSourceOpinions(datasource_id)
    sidebar_filters = json.dumps(
                      {"countries": countries,
                       "stations": rstations,
                       "opinions": opinions})

    context = {
        "name": request.user.username,
        "data_raw": data_js,
        "pie_chart": pie_chart,
        "column_chart": column_chart,
        "data_countries": countries,
        "data_rstations": rstations,
        "data_opinions": opinions,
        "word_freq": word_freq,
        "sidebar_filters": sidebar_filters,
        "title": source.name,
        "table": table
    }

    return render(request, 'main.html', context)


def landing(request):
    return render(request, 'landing.html')


@login_required
def dataManipulation(request, datasource_id):
    data_set = DataSource.objects.get(id=datasource_id).sms_set.all()
    data = []
    for d in data_set:
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'Original': d.text,
                    'Edited': d.modifield_text,
                    'opinion': d.opinion,
                    'Index': d.index,
                    'Language':d.language
                    }
        data.append(instance)
    print datasource_id
    opinions = getDataSourceOpinions(datasource_id=1)

    table = render_to_string("data_edit/table_edit.html",
                             {"data": data, "opinions": opinions,
                              "datasource_id": datasource_id})

    name_form = CreateNameForm()
    dict_form = CreateDictForm()
    return render(request, 'data_edit/data_manipulation.html',
                  {"name": request.user.username, "name_form": name_form,
                   "dict_form": dict_form, "table": table,
                   "datasource_id": datasource_id})


def delD(request, datasource_id):
    data_set = DataSource.objects.get(id=datasource_id).sms_set.all()
    remove_dupes = data_set
    data = []
    for d in data_set:
        remove_dupes = remove_dupes.exclude(Q(country__contains=d.country)& Q(rstation__contains = d.rstation)
            &Q(text__contains=d.text)& ~Q(index__contains=d.index))
    for d in remove_dupes:
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'Original': d.text,
                    'Edited': d.modifield_text, 
                    'opinion': d.opinion,
                    'Index': d.index,
                    'Language':d.language
                    }
        data.append(instance)

    opinions = getDataSourceOpinions(datasource_id)

    table = render_to_string("data_edit/table_edit.html",
                             {"data": data, "opinions": opinions})

    name_form = CreateNameForm()
    dict_form = CreateDictForm()
    return render(request, 'data_edit/data_manipulation.html',
                  {"name_form": name_form, "dict_form": dict_form, "table": table})


def addNameView(request):
    if request.method == 'POST':
        form = CreateNameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            print name
            new_name = Word(word=name, word_type="NAME")
            new_name.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('add_name'))
        else:
            print "not valid form"
    else:
        form = CreateNameForm()  # A empty, unbound form

    # Load documents for the list page
    names = Word.objects.all().filter(word_type="NAME")
    name_list = []
    for name in names:
        name_list.append({"id": name.id, "values": [name.word]})

    headers = ['Name']
    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"title": "Name List", "headers": headers, "list": name_list, 'form': form,
         'name': request.user.username},
        context_instance=RequestContext(request)
    )


def addDictView(request):
    if request.method == 'POST':
        form = CreateDictForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            word = data['word']
            trans = data['trans']
            language = data['language']
            new_dict = Word(word=word, translation=trans,
                            language=language, word_type="DICT")
            new_dict.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('add_dict'))
        else:
            print "not valid form"
    else:
        form = CreateDictForm()  # A empty, unbound form

    # Load documents for the list page
    dicts = Word.objects.all().filter(word_type="DICT")
    dict_list = []
    for d in dicts:
        dict_list.append({"id": d.id, "values": [d.word, d.language, d.translation]})

    headers = ['Word', 'Language', 'Translation']

    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"title": "Dict List", "headers": headers, "list": dict_list, 'form': form,
         'name': request.user.username},
        context_instance=RequestContext(request)
    )


def addSkipView(request):
    if request.method == 'POST':
        form = CreateSkipForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            word = data['word']
            trans = data['trans']
            language = data['language']
            new_skip = Word(word=word, translation=trans,
                            language=language, word_type="SKIP")
            new_skip.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('add_skip'))
        else:
            print "not valid form"
    else:
        form = CreateSkipForm()  # A empty, unbound form
    # Load documents for the list page
    skips = Word.objects.all().filter(word_type="SKIP")
    skip_list = []
    for d in skips:
        skip_list.append({"id": d.id, "values": [d.word, d.language, d.translation]})

    headers = ['Word', 'Language', 'Translation']

    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"title": "Skip List", "headers": headers, "list": skip_list, 'form': form,
         'name': request.user.username},
        context_instance=RequestContext(request)
    )

def addTypoView(request):
    if request.method == 'POST':
        form = CreateTypoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            word = data['word']
            trans = data['translation']
            new_typo = Word(word=word, translation=trans, word_type="TYPO")
            new_typo.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('add_typo'))
        else:
            print "not valid form"
    else:
        form = CreateTypoForm()  # A empty, unbound form
    # Load documents for the list page
    typos = Word.objects.all().filter(word_type="TYPO")
    typo_list = []
    for d in typos:
        typo_list.append({"id": d.id, "values": [d.word, d.translation]})

    headers = ['Word', 'Correction']

    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"title": "Typo List", "headers": headers, "list": typo_list, 'form': form,
         'name': request.user.username},
        context_instance=RequestContext(request)
    )
