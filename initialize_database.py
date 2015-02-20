from charlie.analysis.models import Word


skipwords = ['is', 'and', 'because', 'de', 'to', 'it', 'coz', 'of', 'from', 'porque', 'in', 'the', 'an', 'am', 'you']

for word in skipwords:
	Word(word=word, word_type='SKIP').save()
