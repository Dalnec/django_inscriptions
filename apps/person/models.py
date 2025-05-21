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


class Kind(models.Model):
    description = models.CharField(unique=True, max_length=200)
    active = models.BooleanField()

    class Meta:
        db_table = 'Kind'
        verbose_name = "Kind"
        verbose_name_plural = "Kinds"


class Person(TimeStampedModel):
    GENDER_CHOICES = [
        ("F", "FEMENINO"),
        ("M", "MASCULINO"),
    ]

    code = models.CharField(max_length=20, blank=True, null=True)
    doc_num = models.CharField(max_length=15)
    names = models.CharField(max_length=100)
    lastnames = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True )
    birthdate = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    # kind = models.CharField(max_length=80, blank=True, null=True)
    documenttype = models.ForeignKey(DocumentType, models.DO_NOTHING, blank=True, null=True, related_name='fk_PersonDocument')
    church = models.ForeignKey(Church, models.SET_NULL, blank=True, null=True, related_name='fk_PersonChurch')
    user = models.ForeignKey('user.User', models.CASCADE, blank=True, null=True, related_name='fk_PersonUser')
    kind = models.ForeignKey('Kind', models.SET_NULL, blank=True, null=True, related_name='fk_PersonKind')
    # returned = models.ArrayField()

    def save(self, **kwargs):
        self.names = self.names.upper()
        self.lastnames = self.lastnames.upper()
        super(Person, self).save()

    class Meta:
        db_table = 'Person'
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
    
    def __str__(self):
        return f"{self.doc_num} {self.names} {self.lastnames}"
    
    @property
    def fullname(self):
        return f"{self.names} {self.lastnames}"
    
    def generate_code(self):
        latest = Person.objects.order_by('-id').first()
        next_number = latest.id if latest else 1
        return f"P{next_number:04d}"
    
    # @property
    # def countReturns(self):
    #     return len(self.returned)