from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


admin.site.register(Church)
admin.site.register(DocumentType)
admin.site.register(Person)
admin.site.register(Kind)