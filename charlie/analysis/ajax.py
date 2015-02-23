import json
from models import DataSource, Word, SMS
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


def update_manipulated(request, datasource_id):
    if request.method == 'POST':
        change_list = request.POST.getlist('changes[]')
        for change_item in change_list:
            elem = json.loads(change_item)
            index = elem['index']
            opinion = elem['opinion']
            sms = elem['sms']
            datasource = DataSource.objects.get(id=datasource_id)
            edited_sms = datasource.sms_set.get(index=index)
            edited_sms.opinion = opinion
            edited_sms.modifield_text = sms
            edited_sms.save()
            datasource.modified = True
            datasource.save()
        return HttpResponse("Update successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


def update(request, datasource_id):
    if request.method == 'POST':
        index = request.POST.get('index')
        opinion = request.POST.get('opinion')
        datasource = DataSource.objects.get(id=datasource_id)
        sms = datasource.sms_set.get(index=index)
        sms.opinion = opinion
        sms.save()
        datasource.modified = True
        datasource.save()

        return HttpResponse(
                            json.dumps({'text': sms.opinion}),
                            content_type='application/json'
                            )
    else:
        return HttpResponse("haha")


@login_required
def addName(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        new_name = Word(word=name, word_type="NAME")
        new_name.save()
        print "new name created", name
        return HttpResponse(
                            json.dumps({'text': "new name entry made"}),
                            content_type='application/json'
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
                            content_type='application/json'
                            )
    else:
        return HttpResponse("Creating dictionary entry failed")


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


@login_required
def downloadFile(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    if datasource.modified is True:
        from utils import updateFile
        if updateFile(datasource) == True:
            datasource.modified = False
        else:
            raise Exception("update file not successful")

    file = DataSource.objects.get(id=datasource_id).docfile
    response = HttpResponse(file, content_type="application/csv")
    response['Content-Disposition'] = 'attachment; filename = "bla.csv"'
    return response