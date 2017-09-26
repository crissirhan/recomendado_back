# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 22:34
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateTimeField()),
                ('expire_date', models.DateTimeField()),
                ('job', models.CharField(choices=[('plumb', 'Plumbing'), ('clean', 'Cleaning'), ('elect', 'Electrical technician'), ('lock', 'Locksmithing'), ('gard', 'Gardening'), ('const', 'Construction'), ('forn', 'Forniture making')], max_length=5)),
                ('location', models.CharField(max_length=50)),
                ('availability', multiselectfield.db.fields.MultiSelectField(choices=[('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'), ('thurs', 'Thursday'), ('frid', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=30)),
                ('movility', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Professional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12)),
                ('region', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=100)),
                ('house_number', models.IntegerField()),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')])),
                ('identification', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professional', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comment', models.CharField(max_length=10000, null=True)),
                ('date', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Client')),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Professional')),
            ],
        ),
        migrations.AddField(
            model_name='announcement',
            name='professional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Professional'),
        ),
    ]
