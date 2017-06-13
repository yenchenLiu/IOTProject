# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 08:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MapSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('site_class', models.CharField(max_length=31)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('range', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='map_site', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
