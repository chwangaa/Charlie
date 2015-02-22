# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template.loader import render_to_string
from table import NameTable, DictTable
from models import DataSource, SMS, Word
from forms import DataUploadForm, CreateWordForm, CreateDictForm
from utils import initializeDatabaseForDataSource, getCount
from django.views.generic.edit import UpdateView,CreateView
from django_tables2 import RequestConfig
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
            newdoc = DataSource(
                docfile=request.FILES['docfile'], name=question,
                owner=request.user)
            newdoc.save()

            initializeDatabaseForDataSource(newdoc, answers_raw)
            source_id = newdoc.id
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('analysis', args=[source_id]))
        else:
            return render_to_response('dashboard.html', {'form': form, 'name': request.user.username},
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


@login_required
def delete_datasource(request): 
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        # TODO(Daria): Check this is performed successfully, and send appropriate response.
        data_source = DataSource.objects.get(pk=document_id)
        SMS.objects.filter(source=data_source).delete()
        data_source.delete()
        return HttpResponse("Deletion successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


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
    texts = ""
    for d in sms_set:
        texts = texts + d.modifield_text + " "
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'SMS': d.text,
                    'opinion': d.opinion,
                    'modified_text': d.modifield_text,
                    'Index': d.index}
        data.append(instance)

    # get data for text_display_view
    from utils import getDataSourceOpinions
    opinions = getDataSourceOpinions(datasource_id)
    table = render_to_string("table.html", {"data": data, "opinions": opinions})
    
    # get data for word_cloud_view
    from utils import getFrequencyList
    word_freq = json.dumps(getFrequencyList(texts))

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
    column_chart_data = {"data": data_list, "title": title, "countries": countries}
    column_chart = render_to_string("column_chart.html", column_chart_data)
    
    # get the country list and rstation list for sidebar
    countries = sms_set.values_list('country', flat=True).distinct()
    countries = [str(e) for e in countries]
    rstations = sms_set.values_list('rstation', flat=True).distinct()
    rstations = [str(e) for e in rstations]
    opinions = getDataSourceOpinions(datasource_id)
    sidebar_filters = json.dumps(
                      {"countries": countries, "stations": rstations, "opinions": opinions})

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


def table_view(request, datasource_id):
    data_set = DataSource.objects.get(id=datasource_id).sms_set.all()
    data = []
    for d in data_set:
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'SMS': d.text,
                    'opinion': d.opinion}
        data.append(instance)
    data_js = json.dumps(data)

    return render(request, 'table.html', {"data": data_js})


def landing(request):
    return render(request, 'landing.html')


def update_manipulated(request, datasource_id):
    if request.method == 'POST':
        change_list = request.POST.getlist('changes[]');
        for change_item in change_list:
            elem = json.loads(change_item)
            index = elem['index']
            opinion = elem['opinion']
            sms = elem['sms']
            edited_sms = DataSource.objects.get(id=datasource_id).sms_set.get(index=index)
            edited_sms.opinion=opinion
            edited_sms.modifield_text=sms
            edited_sms.save()
        return HttpResponse("Update successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


def update(request, datasource_id):
    if request.method == 'POST':
        index = request.POST.get('index')
        opinion = request.POST.get('opinion')
        print index
        sms = DataSource.objects.get(id=datasource_id).sms_set.get(index=index)
        sms.opinion = opinion
        sms.save()

        return HttpResponse(
                            json.dumps({'text': sms.opinion}),
                            content_type = 'application/json'
                            )
    else:
        return HttpResponse("haha")


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
                    }
        data.append(instance)

    # get the existing labels
    opinions_raw = data_set.values_list('opinion',flat=True).distinct()

    # cast from ustr to str
    opinions = [str(o) for o in opinions_raw]
    if 'irrelevant' not in opinions:
        opinions.append('irrelevant')

    table = render_to_string("data_edit/table_edit.html",
                             {"data": data, "opinions": opinions})

    name_form = CreateWordForm()
    dict_form = CreateDictForm()
    return render(request, 'data_edit/data_manipulation.html',
                  {"name": request.user.username, "name_form": name_form, "dict_form": dict_form, "table": table})

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
                    }
        data.append(instance)

    # get the existing labels
    opinions_raw = data_set.values_list('opinion',flat=True).distinct()

    # cast from ustr to str
    opinions = [str(o) for o in opinions_raw]
    if 'irrelevant' not in opinions:
        opinions.append('irrelevant')

    table = render_to_string("data_edit/table_edit.html",
                             {"data": data, "opinions": opinions})

    name_form = CreateWordForm()
    dict_form = CreateDictForm()
    return render(request, 'data_edit/data_manipulation.html',
                  {"name_form": name_form, "dict_form": dict_form, "table": table})


def addNameView(request):
    if request.method == 'POST':
        form = CreateWordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            print name
            new_name = Word(word=name, word_type="NAME")
            new_name.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print "not valid form"
    else:
        form = CreateWordForm()  # A empty, unbound form

    # Load documents for the list page
    names = Word.objects.all().filter(word_type="NAME")
    table = NameTable(names)
    RequestConfig(request, paginate=False).configure(table)

    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"table": table, 'form': form, 'name': request.user.username},
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
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print "not valid form"
    else:
        form = CreateDictForm()  # A empty, unbound form

    # Load documents for the list page
    trans = Word.objects.all().filter(word_type="DICT")
    table = DictTable(trans)
    RequestConfig(request, paginate=False).configure(table)

    # Render list page with the documents and the form
    return render_to_response(
        'data_edit/create_single.html',
        {"table": table, 'form': form, 'name': request.user.username},
        context_instance=RequestContext(request)
    )


@login_required
def addName(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_name = Word(word=name, word_type="NAME")
        new_name.save()
        print "new name created", name
        return HttpResponse(
                            json.dumps({'text': "new name entry made"}),
                            content_type = 'application/json'
                            )
    else:
        return HttpResponse("Creating Name Failed")


@login_required
def addDict(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        trans = request.POST.get('trans')
        lang = request.POST.get('lang')
        new_dict = Word(word=word, language=lang, translation=trans,
                        word_type="DICT")
        new_dict.save()
        print "new name created", new_dict

        return HttpResponse(
                            json.dumps({'text': "new dict entry made"}),
                            content_type = 'application/json'
                            )
    else:
        return HttpResponse("Creating dictionary entry failed")
