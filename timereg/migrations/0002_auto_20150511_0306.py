# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftDefaults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('length', models.DurationField()),
            ],
        ),
        migrations.AlterField(
            model_name='shift',
            name='length',
            field=models.DurationField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='shiftfragment',
            name='length',
            field=models.DurationField(editable=False, blank=True),
        ),
    ]
