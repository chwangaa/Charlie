from models import Word


def getLabels(setofLabels):
    # get a set like (("aids": "sida"), ("aids": "bla"))
    # return a dict {"aids": "aids sida bla"}
    labels = {}
    for i, j in setofLabels:
        labels[i] = i
    for i, j in setofLabels:
        labels[i] = labels[i] + "#@#" + j

    return labels


def cleanForWordCloud(text):

    replace_list = Word.objects.all().filter(word_type__in=['TYPO', 'DICT'])
    removes = Word.objects.all().filter(word_type__in=[
                'NAME', 'SKIP']).values_list('word', flat=True)
    replaces = replace_list.values_list('word', flat=True)

    text = text.replace(".", " ")
    words = text.split()
    words_modified = []

    list_words_replaced = set()

    for w in words:
        if len(w) == 1:
            continue
        if w in replaces:
            correction = replace_list.filter(word=w)[0]
            correction = str(correction.translation)
            list_words_replaced.add((correction, str(w)))
            w = correction
        if w in removes:
            continue
        if w.isdigit() and w.isalnum():
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)

    labels = getLabels(list_words_replaced)

    return labels, new_text


def applyCustomizedRules(text):

    names = Word.objects.all().filter(word_type="NAME").values_list(
                'word', flat=True)
    names = [name.lower() for name in names]
    typos = Word.objects.all().filter(word_type="TYPO").values_list(
                'word', flat=True)

    text = text.replace(".", " ")
    words = text.split()
    words_modified = []

    for w in words:
        if w in names:
            w = w.replace(w, "#NE")
            continue
        if w in typos:
            correction = str(typos.filter(word=w)[0])
            words_modified.append(correction)
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text


def removeNonAlphabets(text):
    # to lower case
    import re
    text = text.lower()
    # remove non alphanumberical characters
    text = re.sub(r'[^\w]', ' ', text)
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # remove any space at the front
    text = text.lstrip()
    return deleteNumbers(text)


def replaceName(text, replaceSymbol):
    names = Word.objects.all().filter(word_type="NAME").values_list(
                'word', flat=True)
    text = text.replace(".", " ")
    words = text.split()
    words_modified = []
    names = [name.lower() for name in names]
    for w in words:
        if w in names:
            w = w.replace(w,replaceSymbol)
            words_modified.append(w)
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text


def deleteSkipWords(text):
    skips = Word.objects.all().filter(word_type="SKIP").values_list(
                'word', flat=True)
    words = text.split()
    words_modified = []
    for w in words:
        if w in skips:
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text


def deleteSingleWord(text):
    words = text.split()
    words_modified = []
    for w in words:
        if len(w) == 1:
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text


def deleteNumbers(text):
    words = text.split()
    words_modified = []
    for w in words:
        if w.isdigit() and w.isalnum():
            continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text


def replaceSlangWords(text):
    typos = Word.objects.all().filter(word_type="TYPO")
    typo_names = Word.objects.all().filter(word_type="TYPO").values_list(
                 'word', flat=True)
    words = text.split()
    words_modified = []
    for w in words:
        if w in typo_names:
            for d in typos:
                if w==d.word:
                    w = w.replace(w,d.translation)
                    words_modified.append(w)
                else:
                    continue
        else:
            words_modified.append(w)
    new_text = ' '.join(words_modified)
    return new_text

# this should enable 'sida' and 'aids' to be shown together
def translate(text):
    # TODO
    return text
