# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PrismaMigrations(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    checksum = models.CharField(max_length=64)
    finished_at = models.DateTimeField(blank=True, null=True)
    migration_name = models.CharField(max_length=255)
    logs = models.TextField(blank=True, null=True)
    rolled_back_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField()
    applied_steps_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = '_prisma_migrations'


class Church(models.Model):
    description = models.CharField(unique=True, max_length=200)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'church'


class Documenttype(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(unique=True, max_length=200)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'documenttype'


class Inscription(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    checkinat = models.DateTimeField(db_column='checkinAt', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    countgroup = models.IntegerField()
    vouchergroup = models.CharField(max_length=100)
    voucherpath = models.CharField(max_length=255)
    voucheramount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    personid = models.ForeignKey('Person', models.DO_NOTHING, db_column='personId')  # Field name made lowercase.
    paymentmethodid = models.ForeignKey('Paymentmethod', models.DO_NOTHING, db_column='paymentMethodId', blank=True, null=True)  # Field name made lowercase.
    observations = models.CharField(max_length=255, blank=True, null=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inscription'


class Paymentmethod(models.Model):
    description = models.CharField(unique=True, max_length=50)
    account = models.CharField(max_length=50, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'paymentmethod'


class Person(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    code = models.CharField(max_length=20, blank=True, null=True)
    doc_num = models.CharField(unique=True, max_length=15)
    names = models.CharField(max_length=100)
    lastnames = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    type_person = models.TextField(blank=True, null=True)  # This field type is a guess.
    documenttype = models.ForeignKey(Documenttype, models.DO_NOTHING, blank=True, null=True)
    church = models.ForeignKey(Church, models.DO_NOTHING, blank=True, null=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'person'


class Profile(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class User(models.Model):
    email = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)
    profileid = models.ForeignKey(Profile, models.DO_NOTHING, db_column='profileId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'
