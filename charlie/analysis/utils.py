import csv
from models import SMS


def parseAnswer(answer):
    # remove extra spaces
    answer = answer.replace(' ', '')
    groups = answer.split(';')
    # answer holds the return value
    answers = {}
    for group in groups:
        name = group.split(':')[0]
        options = group.split(':')[1].split(',')
        for option in options:
            option = option.lower()
            answers[option] = name

    return answers


def initializeDatabaseForDataSource(source, answer):
    csv_file_name = source.docfile.path
    csv_file = open(csv_file_name, 'r')
    csv_dict = csv.DictReader(csv_file)

    dictionary = parseAnswer(answer)
    interested_kwards = dictionary.keys()

    for sms in csv_dict:
        import re
        # to lower case
        original_msg = sms['SMS'].lower()
        # remove non alphanumberical characters
        text = re.sub(r'[^\w]', ' ', original_msg)
        # remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        opinion_found = False
        for kw in interested_kwards:
            if kw in text:
                opinion = dictionary[kw]
                opinion_found = True
                break
        if not opinion_found:
            opinion = 'unknown'

        text = sms['SMS'].lower()
        rstation = sms['RStation'].lower()
        country = sms['Country'].lower()
        index = sms['Index']
        s = SMS(text=text, rstation=rstation, country=country,
                source=source, opinion=opinion, index=index)
        s.save()


def getCount(list_values):
    from collections import Counter
    c = Counter(list_values)
    d = dict(c)
    results = []
    for key in d:
        results.append([str(key), d[key]])
    return results


def getFrequencyList(str):
    from collections import Counter
    import re
    # to lower case
    text = str.lower()
    # remove non alphanumberical characters
    text = re.sub(r'[^\w]', ' ', text)
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    words = text.split()
    freq = dict(Counter(words))
    freq_list = []
    for key in freq:
        freq_list.append({"text": key, "weight": freq[key]})
    return sorted(freq_list, key=lambda e: -e['weight'])
