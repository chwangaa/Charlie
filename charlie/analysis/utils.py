import csv
from models import SMS, DataSource, Word
from modification_rules import applyCustomizedRules, cleanForWordCloud
import lang
from django.db import transaction


def initializeDatabaseForDataSource(source, answer):
    csv_file_name = source.docfile.path
    csv_file = open(csv_file_name, 'r')
    csv_dict = csv.DictReader(csv_file)

    dictionary = answer
    interested_kwards = dictionary.keys()
    possible_matchings = Word.objects.filter(word_type='DICT').values_list(
                            'translation', flat=True)
    all_trans = Word.objects.filter(word_type='DICT')
    for word in interested_kwards:
        if word in possible_matchings:
            correction = all_trans.filter(translation=word)[0]
            correction = str(correction.word)
            interested_kwards.append(correction)
            dictionary[correction] = word

    with transaction.atomic():
        for sms in csv_dict:
            import re
            original_msg = sms['SMS']
            # remove non alphanumberical characters
            original_msg = re.sub(r'[^\w]', ' ', original_msg)
            # remove extra spaces
            original_msg = re.sub(r'\s+', ' ', original_msg)
            # to lower case
            text = original_msg.lower()
            # remove any space at the front
            text = text.strip()
            # apply rules
            text = applyCustomizedRules(text)
            if text == "":
                continue
            text = " " + text + " "
            opinion_found = False
            for kw in interested_kwards:
                matching = " " + kw + " "
                if matching in text:
                    opinion = dictionary[kw]
                    opinion_found = True
                    break
            if not opinion_found:
                opinion = 'unknown'

            rstation = sms['RStation'].lower()
            country = sms['Country'].lower()
            index = sms['Index']
            g_lang = lang.guess(text)
            text = text.strip()
            s = SMS(text=text, rstation=rstation, country=country,
                    source=source, opinion=opinion, index=index,
                    modifield_text=text, language=g_lang)
            s.save()
    source.modified = False
    source.save()
    # write the modified back to the file
    updateFile(source)


def getCount(list_values):
    from collections import Counter
    c = Counter(list_values)
    d = dict(c)
    results = []
    for key in d:
        results.append([str(key), d[key]])
    return results


def getFrequencyList(datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    sms_set = source.sms_set.all()

    text = ""
    for d in sms_set:
        text = text + d.modifield_text + " "

    return getFreq(text)


def getFreq(texts):
    synonyms, text = cleanForWordCloud(texts)
    from collections import Counter
    words = text.split()
    freq = dict(Counter(words))
    freq_list = []
    for key in freq:
        if key in synonyms:
            freq_list.append({"text": key, "weight": freq[key],
                              "label": synonyms[key]})
        else:
            freq_list.append({"text": key, "weight": freq[key],
                              "label": key})

    freq_list = sorted(freq_list, key=lambda e: -e['weight'])
    return freq_list


def renderOpinion(opinions_raw):
    opinions = {}
    for key, value in opinions_raw.iteritems():
        opinions[value] = 1

    unique_opinions = ""
    for key in opinions.keys():
        unique_opinions = unique_opinions+key+","
    unique_opinions = unique_opinions+'unknown,irrelevant'
    return unique_opinions


def getDataSourceOpinions(datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    opinions_str = source.opinions
    # get the existing labels
    opinions = opinions_str.split(',')
    # cast from ustr to str
    opinions = [str(o) for o in opinions]

    return opinions


def getOpinionCountryBreakDown(datasource_id):
    source = DataSource.objects.get(id=datasource_id)
    sms_set = source.sms_set.all()

    country_list = sms_set.values_list('country', flat=True).distinct()
    countries = [str(e) for e in country_list]
    opinions = sms_set.values_list('opinion', flat=True).distinct()
    data_list = []
    data_list.append(countries)
    for opinion in opinions:
        # get all messages from this country
        opinion_sms = sms_set.filter(opinion=opinion)
        counts = []
        for country in countries:
            x = opinion_sms.filter(country=country).count()
            counts.append(x)
        data_list.append({"name": str(opinion), "data": counts})
    return data_list


def updateFile(datasource):
    headings = ['Index', 'Country', 'RStation',
                'Text', 'Language', 'Opinion']

    sms_set = datasource.sms_set.all()
    # data is what to write to the file
    data = []
    # append the heading to the data
    data.append(headings)
    # iterate the sms set, append everything to the data
    for sms in sms_set:
        index = sms.index
        country = sms.country.encode('utf-8')
        rstation = sms.rstation.encode('utf-8')
        text = sms.text.encode('utf-8')
        language = sms.language.encode('utf-8')
        opinion = sms.opinion.encode('utf-8')
        entry = [index, country, rstation, text, language, opinion]
        data.append(entry)

    csv_file_path = datasource.docfile.path
    with open(csv_file_path, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

    return True
