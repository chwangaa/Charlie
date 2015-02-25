import json
from models import DataSource, Word, SMS
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import lang


@login_required
def update_manipulated(request, datasource_id):
    if request.method == 'POST':
        change_list = request.POST.getlist('changes[]')
        datasource = DataSource.objects.get(id=datasource_id)
        sms_set = datasource.sms_set
        for change_item in change_list:
            elem = json.loads(change_item)
            index = elem['index']
            opinion = elem['opinion']
            sms = elem['sms']
#           language = elem['lang']
            edited_sms = sms_set.get(index=index)
            edited_sms.opinion = opinion
            edited_sms.modifield_text = sms
            edited_sms.text = sms
#           lang.teach(sms,language)
            edited_sms.save()

        if datasource.modified is True:
            for sms in sms_set.all():
                sms.text = sms.modifield_text
                sms.save()
            datasource.modified = False
            datasource.save()
        return HttpResponse("Update successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


@login_required
def deleteSMS(request, datasource_id):
    if request.method == 'POST':
        checked_list = request.POST.getlist('checked_list[]')
        datasource = DataSource.objects.get(id=datasource_id)
        sms_set = datasource.sms_set
        for item in checked_list:
            sms_id = int(item)
            sms_set.get(index=sms_id).delete()
        return HttpResponse("deletion successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


@login_required
def deleteWord(request):
    if request.method == 'POST':
        word_id = int(request.POST.get('word_id'))
        Word.objects.get(id=word_id).delete()
        return HttpResponse(
                            json.dumps({'text': "deleted"}),
                            content_type='application/json'
                            )
    else:
        return HttpResponse("Deletion Failed")


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
        data_source = DataSource.objects.get(pk=document_id)
        SMS.objects.filter(source=data_source).delete()
        data_source.delete()
        return HttpResponse("Deletion successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


@login_required
def downloadFile(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    from utils import updateFile
    if updateFile(datasource) == False:
        raise Exception("update file not successful")

    file = datasource.docfile
    name = 'attachment; filename = "' + datasource.name + '.csv"'
    response = HttpResponse(file, content_type="application/csv")
    response['Content-Disposition'] = name
    return response
