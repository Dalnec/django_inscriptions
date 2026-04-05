from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from model_utils.models import TimeStampedModel


def default_settings():
    return {
        "inscription": {
            "send_email": True,
            "emails": [
                "daleonco_1995@hotmail.com",
            ],
        },
    }


class Tag(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug (URL Friendly)")
    color = models.CharField(max_length=7, default="#3b82f6", verbose_name="Color (Hex)")

    class Meta:
        db_table = "Tag"
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Activity(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(blank=True, null=True, default=default_settings)
    shortname = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="activities", verbose_name="Etiquetas")

    class Meta:
        db_table = "Activity"
        verbose_name = "Actividad o Evento"
        verbose_name_plural = "Actividades o Eventos"

    def __str__(self):
        return self.title

    @property
    def is_ended(self):
        return self.end_date < timezone.now()

    @property
    def send_email(self):
        return self.settings.get("inscription", {}).get("send_email", False)

    @property
    def emails(self):
        return self.settings.get("inscription", {}).get("emails", [])
