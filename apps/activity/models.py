from model_utils.models import TimeStampedModel
from django.db import models

def default_settings():
    return {
        'inscription': {
            'send_email': True,
            'emails': [
                'daleonco_1995@hotmail.com',
            ],
        },
    }

class Activity(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    settings = models.JSONField(blank=True, null=True, default=default_settings)

    class Meta:
        db_table = 'Activity'
        verbose_name = "Actividad o Evento"
        verbose_name_plural = "Actividades o Eventos"

    def __str__(self):
        return self.title
    
    @property
    def is_past(self):
        return False
        # return self.end_date < timezone.now()
    
    @property
    def send_email(self):
        return self.settings.get('inscription', {}).get('send_email', False)
    
    @property
    def emails(self):
        return self.settings.get('inscription', {}).get('emails', [])
