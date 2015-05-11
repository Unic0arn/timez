# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0002_auto_20150511_0306'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftDefault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('length', models.DurationField()),
            ],
        ),
        migrations.DeleteModel(
            name='ShiftDefaults',
        ),
    ]
