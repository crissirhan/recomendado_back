# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Client(User):
    pass

class Professional(User):
    profession = models.CharField(max_length=100)

class Review(models.Model):
    client = models.ForeignKey('Client')
    professional = models.ForeignKey('Professional')
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.CharField(max_length=10000, null=True)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return 'Review de: ' + self.client.name + ' a: ' + self.professional.name
