from models import Word


def applyCustomizedRules(text):
    text = replaceName(text, "NE")
    text = deleteSkipWords(text)
    text = deleteSingleWord(text)
    return text


def replaceName(text, replaceSymbol):
    return text


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


# this should enable 'sida' and 'aids' to be show together
def translate(text):
    return text
