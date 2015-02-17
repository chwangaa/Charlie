import django_tables2 as tables


class WordTable(tables.Table):
    word = tables.Column(accessor='word', verbose_name='Text')
    word_type = tables.Column(accessor='word_type', verbose_name='Type')

    class Meta:
    	attrs = {"id": "pretty"}