import csv
from models import SMS, DataSource
from modification_rules import applyCustomizedRules
import lang


def initializeDatabaseForDataSource(source, answer):
    csv_file_name = source.docfile.path
    csv_file = open(csv_file_name, 'r')
    csv_dict = csv.DictReader(csv_file)

    dictionary = answer
    interested_kwards = dictionary.keys()

    for sms in csv_dict:
        import re
        # to lower case
        original_msg = sms['SMS'].lower()
        # remove non alphanumberical characters
        text = re.sub(r'[^\w]', ' ', original_msg)
        # remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        # remove any space at the front
        text = text.lstrip()
        # apply rules
        text = applyCustomizedRules(text)
        opinion_found = False
        for kw in interested_kwards:
            if kw in text:
                opinion = dictionary[kw]
                opinion_found = True
                break
        if not opinion_found:
            opinion = 'unknown'

        rstation = sms['RStation'].lower()
        country = sms['Country'].lower()
        index = sms['Index']
        s = SMS(text=original_msg, rstation=rstation, country=country,
                source=source, opinion=opinion, index=index,
                modifield_text=text,language=lang.guess(text))
        s.save()

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
        text = text + applyCustomizedRules(d.modifield_text) + " "

    from collections import Counter

    words = text.split()
    freq = dict(Counter(words))
    freq_list = []
    for key in freq:
        freq_list.append({"text": key, "weight": freq[key]})
    return sorted(freq_list, key=lambda e: -e['weight'])


def renderOpinion(opinions_raw):
    opinions = {}
    for key, value in opinions_raw.iteritems():
        opinions[value] = 1
    print opinions
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
                'Text', 'Modified', 'Opinion']

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
        modified_text = sms.modifield_text.encode('utf-8')
        opinion = sms.opinion.encode('utf-8')
        entry = [index, country, rstation, text, modified_text, opinion]
        data.append(entry)

    csv_file_path = datasource.docfile.path
    with open(csv_file_path, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

    return True
