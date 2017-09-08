# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        abstract = True

class Client(User):
    pass

class Professional(User):
    profession = models.CharField(max_length=100)
