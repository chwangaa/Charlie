from charlie.analysis.models import Word


skipwords = ['is', 'and', 'because', 'de', 'to', 'it', 'coz', 'of', 'from', 'porque', 'in', 'the', 'an', 'am', 'you']

names = ['PETER', 'HARRY', 'Gabriel', 'Esmael', 'Getrud', 'sinda','fredrick']

for word in skipwords:
	Word(word=word, word_type='SKIP').save()

for word in names:
	Word(word=word, word_type='NAME').save()