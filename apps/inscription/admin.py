from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


admin.site.register(Inscription)
admin.site.register(InscriptionGroup)
admin.site.register(Tarifa)
admin.site.register(PaymentMethod)