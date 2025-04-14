from model_utils.models import TimeStampedModel
from django.db import models

class PaymentMethod(models.Model):
    description = models.CharField(unique=True, max_length=50)
    account = models.CharField(max_length=50, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        db_table = 'PaymentMethod'
        verbose_name = "Metedo de Pago"
        verbose_name_plural = "Metodos de Pagos"

class Tarifa(TimeStampedModel):
    description = models.CharField(unique=True, max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField()

    class Meta:
        db_table = 'Tarifa'
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"


class InscriptionGroup(TimeStampedModel):
    vouchergroup = models.CharField(max_length=100)
    voucherfile = models.ImageField(upload_to='vouchers/', blank=True, null=True)
    voucheramount = models.DecimalField(max_digits=10, decimal_places=2)
    activity = models.ForeignKey('activity.Activity', models.CASCADE, related_name="fk_InscriptionGroupActivity")
    user = models.ForeignKey('user.User', models.CASCADE, blank=True, null=True, related_name="fk_InscriptionGroupUser")
    paymentmethod = models.ForeignKey('PaymentMethod', models.DO_NOTHING, blank=True, null=True, related_name="fk_InscriptionGroupMethod")
    tarifa = models.ForeignKey('Tarifa', models.CASCADE, blank=True, null=True, related_name="fk_InscriptionGroupTarifa")

    class Meta:
        db_table = 'InscriptionGroup'
        verbose_name = "Grupo de Inscripcion"
        verbose_name_plural = "Grupos de Inscripcion"


class Inscription(TimeStampedModel):
    STATUS_INSCRIPTION = [
        ("P", "PENDIENTE"),
        ("R", "REGISTRADO"),
        ("C", "CONFIRMADO"),
        ("E", "ERROR"),
    ]

    checkinat = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_INSCRIPTION, blank=True, null=True )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    observations = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey('InscriptionGroup', models.CASCADE, related_name="fk_InscriptionGroup")
    person = models.ForeignKey('person.Person', models.CASCADE, related_name="fk_InscriptionPerson") 
    # user = models.ForeignKey('user.User', models.CASCADE, blank=True, null=True, related_name="fk_InscriptionUser")

    class Meta:
        db_table = 'Inscription'
        verbose_name = "Inscripcion"
        verbose_name_plural = "Inscripciones"
