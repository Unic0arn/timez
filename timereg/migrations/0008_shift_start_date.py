# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0007_auto_20150608_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 19, 12, 56, 44, 359402)),
            preserve_default=False,
        ),
    ]
