from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import DataSource
import lang
from django.db import transaction


@login_required
def updateLanguages(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    with transaction.atomic():
        for sms in sms_set:
            sms.language = lang.guess(sms.modifield_text)
            sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))


@login_required
def removeSkipWords(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    from modification_rules import deleteSkipWords
    with transaction.atomic():
        for sms in sms_set:
            sms.modifield_text = deleteSkipWords(sms.text)
            sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))


@login_required
def replaceNames(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    from modification_rules import replaceName
    with transaction.atomic():
        for sms in sms_set:
            sms.modifield_text = replaceName(sms.text, "NE")
            sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))


@login_required
def replaceSlang(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    from modification_rules import replaceSlangWords
    with transaction.atomic():
        for sms in sms_set:
            sms.modifield_text = replaceSlangWords(sms.text)
            sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))


@login_required
def removeNonAlphaBetical(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    from modification_rules import removeNonAlphabets
    with transaction.atomic():
        for sms in sms_set:
            sms.modifield_text = removeNonAlphabets(sms.text)
            sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))
