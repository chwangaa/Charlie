import django_tables2 as tables


class NameTable(tables.Table):
    word = tables.Column(accessor='word', verbose_name='Text')
    word_type = tables.Column(accessor='word_type', verbose_name='Type')

    class Meta:
    	attrs = {"id": "pretty"}



class DictTable(tables.Table):
    word = tables.Column(accessor='word', verbose_name='Word')
    lang = tables.Column(accessor='translation', verbose_name='Language')
    trans = tables.Column(accessor='language', verbose_name='Translation')

    class Meta:
    	attrs = {"id": "pretty"}