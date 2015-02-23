from django.contrib import admin
from models import DataSource, SMS, Word
# Register your models here.

admin.site.register(DataSourceAdmin)
admin.site.register(SMS)
admin.site.register(Word)