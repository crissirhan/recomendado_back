# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from users.models import *

# Register your models here.
admin.site.register(Client)
admin.site.register(Professional)
admin.site.register(Review)
