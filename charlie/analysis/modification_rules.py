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
    text = text.replace("."," ")
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
