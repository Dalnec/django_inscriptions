from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class PersonAdmin(admin.ModelAdmin):
    search_fields = ["names", "lastnames", "doc_num"]


admin.site.register(Church)
admin.site.register(DocumentType)
admin.site.register(Person, PersonAdmin)
admin.site.register(Kind)