# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0003_auto_20150511_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftdefault',
            name='end_time',
            field=models.TimeField(default="20:00"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shiftdefault',
            name='length',
            field=models.DurationField(editable=False, blank=True),
        ),
    ]
