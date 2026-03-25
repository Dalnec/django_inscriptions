from django.contrib import admin

from .models import Concept, Movement


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "concept_type", "is_active", "is_internal")
    search_fields = ("description",)
    list_filter = ("concept_type", "is_active", "is_internal")


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("id", "movement_at", "activity", "concept", "amount", "status")
    list_filter = ("status", "concept", "activity")
    search_fields = ("description", "reference")
