# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import DataSource, SMS
from forms import DataUploadForm
from utils import initializeDatabaseForDataSource, getCount
from django.views.generic.edit import UpdateView
try:
    import simplejson
except ImportError:
    import json as simplejson


def dashboard(request):
    # Handle file upload
    if request.method == 'POST':
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            question = data['question']
            answers_raw = data['answer']
            newdoc = DataSource(
                docfile=request.FILES['docfile'], name=question)
            newdoc.save()

            initializeDatabaseForDataSource(newdoc, answers_raw)
            source_id = newdoc.id
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('analysis', args=[source_id]))
    else:
        form = DataUploadForm()  # A empty, unbound form

    # Load documents for the list page
    documents = DataSource.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'dashboard.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


class SMSUpdate(UpdateView):
    model = SMS
    fields = ['country', 'text']
    template_name = 'sms_update_form.html'

    def get_object(self, queryset=None):
        obj = SMS.objects.get(id=1)
        return obj


def analysis(request, datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    sms_set = source.sms_set.all()

    # get the sms_set
    data = []
    # use texts to concat all the messages
    texts = ""
    for d in sms_set:
        texts = texts + d.text
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'SMS': d.text,
                    'opinion': d.opinion,
                    'Index': d.index}
        data.append(instance)
    # get the word frequency list
    from utils import getFrequencyList
    word_freq = simplejson.dumps(getFrequencyList(texts))
    # get the raw data
    data_js = simplejson.dumps(data)
    # get the general opinions
    opinions = sms_set.values_list('opinion', flat=True)
    data = getCount(opinions)
    title = "Overview of Opinions Regarding: " + source.name
    # get pie_chart
    chart = {"data": data, "title": title}
    # get column_chart
    opinions = sms_set.values_list('opinion', flat=True).distinct()
    country_list = sms_set.values_list('country', flat=True).distinct()
    title = "Country Break Down"
    countries = [str(e) for e in country_list]
    data_list = []
    for o in opinions:
        o_data = sms_set.filter(opinion=o)
        c_data = o_data.values_list('country', flat=True)
        data = getCount(c_data)
        data = [e[1] for e in data]
        data_list.append({"name": str(o), "data": data})

    column_chart = {"data": data_list, "title": title, "countries": countries}

    # get the country list and rstation list
    countries = sms_set.values_list('country', flat=True).distinct()
    rstations = sms_set.values_list('rstation', flat=True).distinct()
    countries = [str(e) for e in countries]
    rstations = [str(e) for e in rstations]
    sidebar_filters = simplejson.dumps(
                      {"countries": countries, "stations": rstations})

    context = {
        "data_raw": data_js,
        "chart": chart,
        "column_chart": column_chart,
        "data_countries": countries,
        "data_rstations": rstations,
        "word_freq": word_freq,
        "sidebar_filters": sidebar_filters,
        "title": source.name
    }

    return render(request, 'main.html', context)


def charts(request, datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    sms_set = source.sms_set.all()
    opinions = sms_set.values_list('opinion', flat=True)
    from utils import getCount
    opinions = sms_set.values_list('opinion', flat=True).distinct()
    country_list = sms_set.values_list('country', flat=True).distinct()
    data_list = []
    for o in opinions:
        o_data = sms_set.filter(opinion=o)
        c_data = sms_set.values_list('country', flat=True)
        data = getCount(c_data)
        data = [e[1] for e in data]
        data_list.append({"name": str(o), "data": data})

    countries = [str(e) for e in country_list]
    print countries, "hfkdfjlkajlfkadf"
    column_chart = {"data": data_list, "title": title, "countries": countries}

    return render(request, 'chart.html', {'column_chart': column_chart})


def table_view(request, datasource_id):
    data_set = DataSource.objects.get(id=datasource_id).sms_set.all()
    data = []
    for d in data_set:
        instance = {'Country': d.country,
                    'RStation': d.rstation,
                    'SMS': d.text,
                    'opinion': d.opinion}
        data.append(instance)
    data_js = simplejson.dumps(data)

    return render(request, 'table.html', {"data": data_js})

def landing(request):
    return render(request, 'landing.html')
