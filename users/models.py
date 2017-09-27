# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")

class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professional")
    rut = models.CharField(max_length=12)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    identification = models.ImageField(upload_to='images/', blank=True, null=True)

class Review(models.Model):
    client = models.ForeignKey('Client')
    professional = models.ForeignKey('Professional')
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length=10000, null=True)
    date = models.DateTimeField(null=False)

    def __str__(self):
        #TODO: add proffesional and client names
        return 'Review de: ' + ' para: ' + '. Fecha: ' + self.date.strftime(" %d %B, %Y")

class Announcement(models.Model):
    WEEKDAYS = (('lun', 'Lunes'),
              ('mar', 'Martes'),
              ('mier', 'Miércoles'),
              ('jue', 'Jueves'),
              ('vier', 'Viernes'),
              ('sab', 'Sábado'),
              ('dom', 'Domingo'))

    professional = models.ForeignKey('Professional')
    publish_date = models.DateTimeField(null=False)
    expire_date = models.DateTimeField(null=False)
    job = models.ForeignKey('JobCategory')
    location = models.CharField(max_length=50)
    availability = MultiSelectField(choices=WEEKDAYS, max_choices=7)
    movility = models.CharField(max_length=50)

    def __str__(self):
        return self.professional.user.first_name + ' ' + self.professional.user.last_name + ' publicita trabajo como: ' + self.job.job_type + '. Entre: ' + self.publish_date.strftime(" %d %B, %Y") + ' y ' + self.expire_date.strftime(" %d %B, %Y")

class JobCategory(models.Model):
    job_type = models.CharField(max_length=50)

    def __str__(self):
        return self.job_type

class JobSubCategory(models.Model):
    job_sub_type = models.CharField(max_length=50)
    job_category = models.ForeignKey('JobCategory',related_name='sub_type')

    def __str__(self):
        return self.job_sub_type
