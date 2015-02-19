import pickle
import re

f = open('base_db.dict','rb')
db = pickle.load(f)

def teach(message,lang):
    words = re.findall('\w+', message)
    
    if not db.has_key(lang):
        db[lang] = set()

    words = [word for word in words if len(word) > 2]
    words = [word.lower() for word in words]
    words = set(words) # Uniqueness

    other_langs = [key for key in db.keys() if key != lang]
    for word in words:
        is_there = [word in db[language] for language in other_langs]
        print(is_there)
        if set(is_there) == {False}:
            db[lang].update({word})
            print(lang)

def guess(message):
    langs = db.copy()
    for key in langs.keys():
        langs[key] = 0
    
    words = re.findall('\w+', message)
    words = [word for word in words if len(word) > 2]
    words = [word.lower() for word in words]
    words = set(words) # Uniqueness
    
    for word in words:
        for lang in langs:
            if word in db[lang]:
                langs[lang] += 1
    return langs
