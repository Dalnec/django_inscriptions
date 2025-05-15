from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class PaymentMethodResource(resources.ModelResource):
    class Meta:
        model = PaymentMethod

class PaymentMethodAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PaymentMethodResource

class InscriptionGroupAdmin(admin.ModelAdmin):
    search_fields = ["activity__name", "inscription__person__names", "inscription__person__lastnames"]

class InscriptionAdmin(admin.ModelAdmin):
    search_fields = ["person__names", "person__lastnames"]


admin.site.register(Inscription)
admin.site.register(InscriptionGroup)
admin.site.register(Tarifa)
admin.site.register(PaymentMethod, PaymentMethodAdmin)