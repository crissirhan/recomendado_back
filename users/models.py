# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

# Create your models here.

class ExtendedUser(User):
    class Meta:
        abstract = True

class Client(ExtendedUser):
    pass

class Professional(ExtendedUser):
    rut = models.CharField(max_length=12)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    house_number = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    identification = models.ImageField(upload_to='images/', null=True)

class Review(models.Model):
    client = models.ForeignKey('Client')
    professional = models.ForeignKey('Professional')
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length=10000, null=True)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return 'Review from: ' + self.client.name + ' to: ' + self.professional.name + '. Date: ' + self.date.strftime(" %d %B, %Y")

class Announcement(models.Model):
    WEEKDAYS = (('mon', 'Monday'),
              ('tue', 'Tuesday'),
              ('wed', 'Wednesday'),
              ('thurs', 'Thursday'),
              ('frid', 'Friday'),
              ('sat', 'Saturday'),
              ('sun', 'Sunday'))

    professional = models.ForeignKey('Professional')
    publish_date = models.DateTimeField(null=False)
    expire_date = models.DateTimeField(null=False)
    job = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    availability = MultiSelectField(choices=WEEKDAYS, max_choices=7)
    movility = models.CharField(max_length=50)

    def __str__(self):
        return self.professional.name + ' advertises job as: ' + self.job + '. Between: ' + self.publish_date + ' and ' + self.expire_date
