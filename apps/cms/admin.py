from django.contrib import admin
from .models import PageContent, MediaAsset


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ["activity", "page_title", "theme_color", "modified"]
    list_filter = ["theme_color", "created", "modified"]
    search_fields = ["activity__title", "page_title", "hero_motto"]
    readonly_fields = ["created", "modified"]

    fieldsets = (
        (
            "Configuración de Página",
            {
                "fields": ("activity", "page_title", "theme_color", "language"),
            },
        ),
        (
            "Hero",
            {
                "fields": (
                    "hero_motto",
                    "hero_verse",
                    "hero_citation",
                    "hero_date_label",
                    "hero_background_image",
                ),
            },
        ),
        (
            "Sección de Visión",
            {
                "fields": (
                    "vision_title",
                    "vision_description",
                    "vision_feature_1_icon",
                    "vision_feature_1_label",
                    "vision_feature_2_icon",
                    "vision_feature_2_label",
                    "vision_image_1",
                    "vision_image_2",
                ),
            },
        ),
        (
            "Planes de Precios",
            {
                "fields": (
                    "pricing_section_title",
                    "pricing_currency",
                    "plan_1_id",
                    "plan_1_name",
                    "plan_1_price",
                    "plan_1_original_price",
                    "plan_1_subtitle",
                    "plan_1_is_recommended",
                    "plan_1_cta_text",
                    "plan_1_benefits",
                    "plan_2_id",
                    "plan_2_name",
                    "plan_2_price",
                    "plan_2_original_price",
                    "plan_2_subtitle",
                    "plan_2_is_recommended",
                    "plan_2_cta_text",
                    "plan_2_whatsapp_link",
                    "plan_2_benefits",
                ),
            },
        ),
        (
            "Ubicación",
            {
                "fields": (
                    "location_place_name",
                    "location_address",
                    "location_city",
                    "location_description",
                    "location_map_url",
                    "location_amenities",
                ),
            },
        ),
        (
            "Footer",
            {
                "fields": ("footer_cta_title", "footer_organization", "footer_year"),
            },
        ),
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ["original_filename", "activity", "created"]
    list_filter = ["activity"]
    search_fields = ["original_filename", "activity__title"]
    readonly_fields = ["created"]
