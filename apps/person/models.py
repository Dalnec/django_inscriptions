from model_utils.models import TimeStampedModel
from django.db import models

class Church(models.Model):
    description = models.CharField(unique=True, max_length=200)
    active = models.BooleanField()

    class Meta:
        db_table = 'Church'
        verbose_name = "Iglesia"
        verbose_name_plural = "Iglesias"


class DocumentType(models.Model):
    description = models.CharField(unique=True, max_length=200)
    active = models.BooleanField()

    class Meta:
        db_table = 'DocumentType'
        verbose_name = "Tipo Documento"
        verbose_name_plural = "Tipo Documentos"


class Person(TimeStampedModel):
    GENDER_CHOICES = [
        ("F", "FEMENINO"),
        ("M", "MASCULINO"),
    ]

    code = models.CharField(max_length=20, blank=True, null=True)
    doc_num = models.CharField(unique=True, max_length=15)
    names = models.CharField(max_length=100)
    lastnames = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True )
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    kind = models.CharField(max_length=80, blank=True, null=True)
    documenttype = models.ForeignKey(DocumentType, models.DO_NOTHING, blank=True, null=True, related_name='fk_PersonDocument')
    church = models.ForeignKey(Church, models.SET_NULL, blank=True, null=True, related_name='fk_PersonChurch')
    user = models.ForeignKey('user.User', models.CASCADE, blank=True, null=True, related_name='fk_PersonUser')
    # returned = models.ArrayField()

    class Meta:
        db_table = 'Person'
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
    
    @property
    def fullname(self):
        return f"{self.names} {self.lastnames}"
    
    # @property
    # def countReturns(self):
    #     return len(self.returned)