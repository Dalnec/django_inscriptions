from django.db import models
from model_utils.models import TimeStampedModel
from apps.activity.models import Activity


def cms_media_path(instance, filename):
    return f"cms/media/{instance.activity.id}/{filename}"


def cms_hero_path(instance, filename):
    return f"cms/hero/{instance.page_content.activity.id}/{filename}"


class PageContent(TimeStampedModel):
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        related_name="cms_page",
        verbose_name="Actividad",
    )
    page_title = models.CharField(max_length=200, default="")
    theme_color = models.CharField(max_length=7, default="#f97316")
    language = models.CharField(max_length=10, default="es-PE")

    hero_motto = models.CharField(max_length=100, default="")
    hero_verse = models.TextField(default="")
    hero_citation = models.CharField(max_length=100, default="")
    hero_date_label = models.CharField(max_length=50, default="")
    hero_background_image = models.ImageField(
        upload_to=cms_hero_path,
        blank=True,
        null=True,
        verbose_name="Imagen de fondo del Hero",
    )

    vision_title = models.CharField(max_length=200, default="")
    vision_description = models.TextField(default="")
    vision_feature_1_icon = models.CharField(max_length=50, default="")
    vision_feature_1_label = models.CharField(max_length=100, default="")
    vision_feature_2_icon = models.CharField(max_length=50, default="")
    vision_feature_2_label = models.CharField(max_length=100, default="")
    vision_image_1 = models.ImageField(
        upload_to=cms_hero_path,
        blank=True,
        null=True,
        verbose_name="Imagen de visión 1",
    )
    vision_image_2 = models.ImageField(
        upload_to=cms_hero_path,
        blank=True,
        null=True,
        verbose_name="Imagen de visión 2",
    )

    pricing_section_title = models.CharField(max_length=200, default="")
    pricing_currency = models.CharField(max_length=10, default="S/")

    plan_1_id = models.CharField(max_length=50, default="early_bird")
    plan_1_name = models.CharField(max_length=100, default="")
    plan_1_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plan_1_original_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    plan_1_subtitle = models.CharField(max_length=200, default="")
    plan_1_is_recommended = models.BooleanField(default=False)
    plan_1_cta_text = models.CharField(max_length=100, default="")
    plan_1_benefits = models.JSONField(default=list)

    plan_2_id = models.CharField(max_length=50, default="group_promo")
    plan_2_name = models.CharField(max_length=100, default="")
    plan_2_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plan_2_original_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    plan_2_subtitle = models.CharField(max_length=200, default="")
    plan_2_is_recommended = models.BooleanField(default=False)
    plan_2_cta_text = models.CharField(max_length=100, default="")
    plan_2_whatsapp_link = models.URLField(blank=True, default="")
    plan_2_benefits = models.JSONField(default=list)

    location_place_name = models.CharField(max_length=200, default="")
    location_address = models.CharField(max_length=500, default="")
    location_city = models.CharField(max_length=100, default="")
    location_description = models.TextField(default="")
    location_map_url = models.URLField(blank=True, default="")
    location_amenities = models.JSONField(default=list)

    footer_cta_title = models.CharField(max_length=200, default="")
    footer_organization = models.CharField(max_length=200, default="")
    footer_year = models.IntegerField(default=2026)

    class Meta:
        db_table = "cms_page_content"
        verbose_name = "Contenido de Página"
        verbose_name_plural = "Contenidos de Página"

    def __str__(self):
        return f"CMS: {self.activity.title}"


class MediaAsset(TimeStampedModel):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="cms_media_assets",
        verbose_name="Actividad",
    )
    file = models.ImageField(upload_to=cms_media_path, verbose_name="Archivo")
    original_filename = models.CharField(max_length=255)

    class Meta:
        db_table = "cms_media_asset"
        verbose_name = "Archivo Multimedia"
        verbose_name_plural = "Archivos Multimedia"

    def __str__(self):
        return self.original_filename
