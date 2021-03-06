# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from djmoney.models.fields import MoneyField
from django.db.models import Count, Avg

from versatileimagefield.fields import VersatileImageField

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    profile_picture = VersatileImageField(upload_to='images/client_profile_pictures/', blank=True, null=True)

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
    identification = VersatileImageField(upload_to='images/professional_identification/', blank=True, null=True)
    profile_picture = VersatileImageField(upload_to='images/professional_profile_pictures/', blank=True, null=True)
    experience = models.CharField(max_length=2000, blank=True, null=True)

    def average(self):
        return Review.objects.filter(service__announcement__professional__id=self.id).aggregate(Avg('rating'))["rating__avg"]
    def count(self):
        return Review.objects.filter(service__announcement__professional__id=self.id).aggregate(Count('rating'))["rating__count"]

    def __unicode__(self):
        return u'{f}'.format(f=self.user.username)

class Review(models.Model):
    #client = models.ForeignKey('Client', models.CASCADE)
    #professional = models.ForeignKey('Professional', models.CASCADE)
    service = models.ForeignKey('Service', models.CASCADE,related_name='review')
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

    professional = models.ForeignKey('Professional', models.CASCADE,related_name='announcement')
    publish_date = models.DateTimeField(null=False)
    expire_date = models.DateTimeField(null=False)
    location = models.CharField(max_length=50, null=True)
    availability = MultiSelectField(choices=WEEKDAYS, max_choices=7)
    movility = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=3000)
    price = MoneyField(max_digits=10, decimal_places=0, default_currency='CLP', null=True)
    visible = models.BooleanField(default=True)
    approved = models.BooleanField(default=True)
    announcement_thumbnail = VersatileImageField(upload_to='images/announcement_thumbnails/', blank=True, null=True)

    def get_weekdays(self):
        return self.WEEKDAYS
    def professional_rating_average(self):
        return Review.objects.filter(service__announcement__professional__id=self.professional.id).aggregate(Avg('rating'))["rating__avg"]
    def professional_rating_count(self):
        return Review.objects.filter(service__announcement__professional__id=self.professional.id).aggregate(Count('rating'))["rating__count"]
    def __unicode__(self):
        return u'{f}'.format(f=self.professional.user.username + ' publicita trabajo entre: ' + self.publish_date.strftime(" %d %B, %Y") + ' y ' + self.expire_date.strftime(" %d %B, %Y"))

class JobTag(models.Model):
    announcement = models.ForeignKey('Announcement', models.CASCADE,related_name='job_tags')
    job = models.ForeignKey('JobSubCategory', models.CASCADE,related_name='job')

    def __unicode__(self):
        return u'{f}'.format(f='Anuncio: ' + self.announcement.__unicode__() + '. Tipo trabajo: ' + self.job.__unicode__())

class AnnouncementImage(models.Model):
    image = VersatileImageField(upload_to='images/announcement_images/', blank=True, null=True)
    announcement = models.ForeignKey('Announcement', models.CASCADE,related_name='announcement_images')

class JobCategory(models.Model):
    job_type = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    image = VersatileImageField(upload_to='images/job_category/', blank=True, null=True)

    def __unicode__(self):
        return u'{f}'.format(f=self.job_type)

class JobSubCategory(models.Model):
    job_sub_type = models.CharField(max_length=50)
    job_category = models.ForeignKey('JobCategory', models.CASCADE,related_name='sub_type')
    description = models.CharField(max_length=3000, blank=True, null=True)
    image = VersatileImageField(upload_to='images/job_sub_category/', blank=True, null=True)

    def __unicode__(self):
        return u'{f}'.format(f=self.job_sub_type)

class Service(models.Model):
    announcement = models.ForeignKey('Announcement', models.CASCADE,related_name='service')
    client = models.ForeignKey('Client', models.CASCADE,related_name='client')
    cost = MoneyField(max_digits=10, decimal_places=0, default_currency='CLP', null=True)
    creation_date = models.DateTimeField(null=False)
    contacted_date = models.DateTimeField(null=True, blank=True)
    contacted = models.BooleanField(default=False)
    hired = models.BooleanField(default=False)
    hired_date = models.DateTimeField(null=True, blank=True)
    professional_rejected = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'{f}'.format(f=self.announcement.professional.user.username + 'presta servicio a: ' +self.client.user.username )
