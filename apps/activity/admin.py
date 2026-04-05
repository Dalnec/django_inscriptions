from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Activity, Tag


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = ("name", "slug", "color")
    search_fields = ("name", "slug")


@admin.register(Activity)
class ActivityAdmin(ImportExportModelAdmin):
    list_display = ("title", "start_date", "end_date", "is_active", "get_tags")
    list_filter = ("is_active", "tags")
    search_fields = ("title", "description", "shortname")

    def get_tags(self, obj):
        return ", ".join(t.name for t in obj.tags.all())
    get_tags.short_description = "Etiquetas"