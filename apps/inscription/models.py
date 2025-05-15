from model_utils.models import TimeStampedModel
from django.db import models

class PaymentMethod(models.Model):
    description = models.CharField(unique=True, max_length=50)
    account = models.CharField(max_length=50, blank=True, null=True)
    cci = models.CharField(max_length=50, blank=True, null=True)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        db_table = 'PaymentMethod'
        verbose_name = "Metedo de Pago"
        verbose_name_plural = "Metodos de Pagos"
    
    def __str__(self):
        return self.description

class Tarifa(TimeStampedModel):
    description = models.CharField(unique=True, max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    selected = models.BooleanField(default=True)

    class Meta:
        db_table = 'Tarifa'
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"

def path_and_rename(instance, filename):
    upload_to = 'vouchers/'
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}.{}'.format(f'voucher_{instance.activity.id}', instance.vouchergroup, instance.tarifa.description, ext)
    return upload_to + filename

class InscriptionGroup(TimeStampedModel):
    vouchergroup = models.CharField(max_length=100, blank=True, null=True)
    voucherfile = models.ImageField(upload_to=path_and_rename, blank=True, null=True)
    voucheramount = models.DecimalField(max_digits=10, decimal_places=2)
    activity = models.ForeignKey('activity.Activity', models.CASCADE, related_name="fk_InscriptionGroupActivity")
    user = models.ForeignKey('user.User', models.CASCADE, blank=True, null=True, related_name="fk_InscriptionGroupUser")
    paymentmethod = models.ForeignKey('PaymentMethod', models.DO_NOTHING, blank=True, null=True, related_name="fk_InscriptionGroupMethod")
    tarifa = models.ForeignKey('Tarifa', models.CASCADE, blank=True, null=True, related_name="fk_InscriptionGroupTarifa")

    class Meta:
        db_table = 'InscriptionGroup'
        verbose_name = "Grupo de Inscripcion"
        verbose_name_plural = "Grupos de Inscripcion"
    
    def __str__(self):
        return f"{self.vouchergroup} - {self.activity.name}"
    
    def generate_code(self):
        latest = InscriptionGroup.objects.all().order_by('-id').first()
        next_number = latest.id if latest else 1
        return f"G{next_number:04d}"
        # self.vouchergroup = f"G{next_number:04d}"
        # self.save()


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
    
    def __str__(self):
        return f"{self.group.vouchergroup} - {self.person.name} {self.person.lastname} - {self.status_description}"
    
    @property
    def status_description(self):
        return dict(self.STATUS_INSCRIPTION).get(self.status, 'Unknown')
    
    def send_email(self, subject='Inscripción', body=None, from_email='dalnec1405@gmail.com', to_email=['daleonco_1995@hotmail.com']):
        from django.core.mail import EmailMessage

        email = EmailMessage(
            "subject",
            "body",
            from_email,
            to_email,
            # attachments=[
            #     (self.filename, output.getvalue(), 'application/vnd.ms-excel')
            # ]
        )
        email.send()
