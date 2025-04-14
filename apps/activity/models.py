from model_utils.models import TimeStampedModel
from django.db import models

class Activity(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Activity'
        verbose_name = "Actividad o Evento"
        verbose_name_plural = "Actividades o Eventos"

    def __str__(self):
        return self.title