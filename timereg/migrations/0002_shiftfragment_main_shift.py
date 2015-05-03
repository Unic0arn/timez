# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftfragment',
            name='main_shift',
            field=models.ForeignKey(default=1, to='timereg.Shift'),
            preserve_default=False,
        ),
    ]
