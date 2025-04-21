from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class PaymentMethodResource(resources.ModelResource):
    class Meta:
        model = PaymentMethod

class PaymentMethodAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PaymentMethodResource

admin.site.register(Inscription)
admin.site.register(InscriptionGroup)
admin.site.register(Tarifa)
admin.site.register(PaymentMethod, PaymentMethodAdmin)