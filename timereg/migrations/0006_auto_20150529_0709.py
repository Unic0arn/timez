# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0005_auto_20150529_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='shiftdefault',
            name='possible_days',
            field=models.ManyToManyField(to='timereg.Day'),
        ),
    ]
