# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    profile_picture = models.ImageField(upload_to='images/client_profile_pictures/', blank=True, null=True)

    def __unicode__(self):
        return u'{f}'.format(f=self.user.username)

class Professional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="professional")
    rut = models.CharField(max_length=12)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    identification = models.ImageField(upload_to='images/professional_identification/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/professional_profile_pictures/', blank=True, null=True)
    experience = models.CharField(max_length=2000, blank=True, null=True)

    #TODO: add more identification and certification related fields
    def __unicode__(self):
        return u'{f}'.format(f=self.user.username)

class Review(models.Model):
    #client = models.ForeignKey('Client')
    #professional = models.ForeignKey('Professional')
    service = models.ForeignKey('Service')
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    client_comment = models.CharField(max_length=10000, blank=True, null=True)
    professional_response = models.CharField(max_length=10000, blank=True, null=True)
    date = models.DateTimeField(null=False)

    def __unicode__(self):
        return 'Review de: ' + u'{f}'.format(f=self.service.client.user.username) + ' para: ' + u'{f}'.format(f=self.service.announcement.professional.user.username) + '. Fecha: ' + self.date.strftime(" %d %B, %Y")

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
    location = models.CharField(max_length=50)
    availability = MultiSelectField(choices=WEEKDAYS, max_choices=7)
    movility = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=3000)
    price = MoneyField(max_digits=10, decimal_places=0, default_currency='CLP', null=False)
    visible = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    announcement_thumbnail = models.ImageField(upload_to='images/announcement_thumbnails/', blank=True, null=True)

    def get_weekdays(self):
        return self.WEEKDAYS
    def __unicode__(self):
        return u'{f}'.format(f=self.professional.user.username + ' publicita trabajo como: ' + self.job.job_type + '. Entre: ' + self.publish_date.strftime(" %d %B, %Y") + ' y ' + self.expire_date.strftime(" %d %B, %Y"))

class JobTag(models.Model):
    announcement = models.ForeignKey('Announcement')
    job = models.ForeignKey('JobSubCategory')

    def __unicode__(self):
        return u'{f}'.format(f='Anuncio: ' + self.announcement.__unicode__ + '. Tipo trabajo: ' + self.job.__unicode__)

class AnnouncementImage(models.Model):
    image = models.ImageField(upload_to='images/announcement_images/', blank=True, null=True)
    announcement = models.ForeignKey('Announcement')

class JobCategory(models.Model):
    job_type = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/job_category/', blank=True, null=True)

    def __unicode__(self):
        return u'{f}'.format(f=self.job_type)

class JobSubCategory(models.Model):
    job_sub_type = models.CharField(max_length=50)
    job_category = models.ForeignKey('JobCategory',related_name='sub_type')
    description = models.CharField(max_length=3000, blank=True, null=True)
    image = models.ImageField(upload_to='images/job_sub_category/', blank=True, null=True)

    def __unicode__(self):
        return u'{f}'.format(f=self.job_sub_type)

class Service(models.Model):
    announcement = models.ForeignKey('Announcement',related_name='announcement')
    client = models.ForeignKey('Client',related_name='client')
    cost = MoneyField(max_digits=10, decimal_places=0, default_currency='CLP', null=False)
    creation_date = models.DateTimeField(null=False)

    def __unicode__(self):
        return u'{f}'.format(f=self.announcement.professional.user.username + 'presta servicio a: ' +self.client.user.username )
