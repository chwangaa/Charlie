import json
from models import DataSource, Word
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
            edited_sms = DataSource.objects.get(
                id=datasource_id).sms_set.get(index=index)
            edited_sms.opinion = opinion
            edited_sms.modifield_text = sms
            edited_sms.save()
        return HttpResponse("Update successful")
    else:
        return HttpResponseBadRequest("Request should be of POST type.")


def update(request, datasource_id):
    if request.method == 'POST':
        index = request.POST.get('index')
        opinion = request.POST.get('opinion')
        sms = DataSource.objects.get(id=datasource_id).sms_set.get(index=index)
        sms.opinion = opinion
        sms.save()

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
