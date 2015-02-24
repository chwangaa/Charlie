import os
import pickle
import re

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'base_db.dict')

# f = open('/home/swaraj/Code/Python/Charlie/base_db.dict','rb')
# db = pickle.load(f)

def teach(message,lang):
    with open(file_path, "rb") as f:
        db = pickle.load(f)
#   loc = '/home/swaraj/Code/Python/Charlie/base_db.dict'
#   db = pickle.load(open(loc,'rb'))

    words = re.findall('\w+', message)
    
    if not db.has_key(lang):
        db[lang] = set()

    words = [word for word in words if len(word) > 2]
    words = [word.lower() for word in words]
    words = set(words) # Uniqueness

    for word in words:
        for language in db.keys():
            db[language].difference_update({word})

    for word in words:
        db[lang].update({word})

    with open(file_path, "wb") as f:
        pickle.dump(db, f)
#   pickle.dump(db,open(loc,'wb'))


def guess(message):
    with open(file_path, "rb") as f:
        db = pickle.load(f)
#   loc = '/home/swaraj/Code/Python/Charlie/base_db.dict'
#   db = pickle.load(open(loc,'rb'))

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

    best_match = max([(value, key) for key, value in langs.items()])[1]
    is_best_match = True
    for lang in langs.keys():
        if lang != best_match and langs[lang] == langs[best_match]:
            is_best_match = False

    if is_best_match:
        return best_match
    else:
        return 'Unknown'
