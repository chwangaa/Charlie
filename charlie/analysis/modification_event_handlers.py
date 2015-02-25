from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import DataSource
import lang


@login_required
def updateLanguages(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    for sms in sms_set:
        sms.language = lang.guess(modifield_text)
        sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))


@login_required
def removeSkipWords(request, datasource_id):
    datasource = DataSource.objects.get(id=datasource_id)
    datasource.modified = True
    datasource.save()
    sms_set = datasource.sms_set.all()
    from modification_rules import deleteSkipWords
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
    for sms in sms_set:
        sms.modifield_text = removeNonAlphabets(sms.text)
        sms.save()
    return HttpResponseRedirect(reverse('manipulation', args=[datasource_id]))
