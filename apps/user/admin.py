from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import DetailPermission, Permission, Profile, User

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class PermissionResource(resources.ModelResource):
    class Meta:
        model = Permission

class DetailPermissionResource(resources.ModelResource):
    class Meta:
        model = DetailPermission

class ProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProfileResource

class DetailPermissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = DetailPermissionResource

# class PermissionDetail(admin.TabularInline):
#     model = Permission
#     extra = 1

class PermissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PermissionResource
    # inlines = (PermissionDetail,)
    search_fields = ('permission',)

# class PermissionAdmin(admin.ModelAdmin):
#     inlines = (PermissionDetail,)
#     search_fields = ('permission',)

# Register your models here.
admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(DetailPermission, DetailPermissionAdmin)


