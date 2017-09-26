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
        return 'Review from: ' + ' to: ' + '. Date: ' + self.date.strftime(" %d %B, %Y")

class Announcement(models.Model):
    WEEKDAYS = (('mon', 'Monday'),
              ('tue', 'Tuesday'),
              ('wed', 'Wednesday'),
              ('thurs', 'Thursday'),
              ('frid', 'Friday'),
              ('sat', 'Saturday'),
              ('sun', 'Sunday'))

    JOB_CATEGORIES = (('plumb', 'Plumbing'),
              ('clean', 'Cleaning'),
              ('elect', 'Electrical technician'),
              ('lock', 'Locksmithing'),
              ('gard', 'Gardening'),
              ('const', 'Construction'),
              ('forn', 'Forniture making'))

    professional = models.ForeignKey('Professional')
    publish_date = models.DateTimeField(null=False)
    expire_date = models.DateTimeField(null=False)
    job = models.CharField(max_length=5, choices=JOB_CATEGORIES)
    location = models.CharField(max_length=50)
    availability = MultiSelectField(choices=WEEKDAYS, max_choices=7)
    movility = models.CharField(max_length=50)

    def __str__(self):
        return self.professional.first_name + ' ' + self.professional.last_name + ' advertises job as: ' + self.job + '. Between: ' + self.publish_date.strftime(" %d %B, %Y") + ' and ' + self.expire_date.strftime(" %d %B, %Y")
