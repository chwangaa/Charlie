import django_tables2 as tables


class NameTable(tables.Table):
    delete = tables.LinkColumn('addingName', verbose_name='delete', attrs='<input type="checkbox"/>')
    word = tables.Column(accessor='word', verbose_name='Name')

    class Meta:
        attrs = {"id": "pretty"}


class WordTable(tables.Table):
    word = tables.Column(accessor='word', verbose_name='Word')
    lang = tables.Column(accessor='translation', verbose_name='Language')
    trans = tables.Column(accessor='language', verbose_name='Translation')

    class Meta:
        attrs = {"id": "pretty"}