# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('modification', models.DecimalField(max_digits=3, decimal_places=2)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ObSpecials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('oblevel', models.ForeignKey(to='timereg.ObLevel')),
            ],
        ),
        migrations.CreateModel(
            name='ObTimes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('day', models.IntegerField()),
                ('oblevel', models.ForeignKey(to='timereg.ObLevel')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('length', models.DurationField(blank=True)),
                ('worker', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftFragment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('length', models.DurationField()),
                ('main_shift', models.ForeignKey(to='timereg.Shift')),
                ('oblevel', models.ForeignKey(to='timereg.ObLevel')),
                ('worker', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
