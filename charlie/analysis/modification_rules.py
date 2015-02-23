from models import Word


def applyCustomizedRules(text):
    text = replaceName(text, "NE")
    text = deleteSingleWord(text)
    text = replaceSlangWords(text)
    text = deleteNumbers(text)
    text = deleteSkipWords(text)
    # TO_DISCUSS
    # translate(text)
    return text


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
    words = text.split()
    words_modified = []
    for w in words:
        if w in names:
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
    slang_dict = {' bcz ':' because ',' bcoz ':' because ',' 4m ':'from',' 4rm ':'from',
    ' 2 ':' to ', '4':' for ', ' u ':' you ', ' ur ':' your ', ' da ':' the ', ' coz ':' because ', '4rm':' from ',' fo ':' for '}
    for i,j in slang_dict.iteritems():
        text = text.replace(i,j)
    return text

# this should enable 'sida' and 'aids' to be show together
def translate(text):
    # TODO
    return text
