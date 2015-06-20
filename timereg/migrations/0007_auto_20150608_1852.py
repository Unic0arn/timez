# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timereg', '0006_auto_20150529_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obtimes',
            name='day',
        ),
        migrations.AddField(
            model_name='obtimes',
            name='days',
            field=models.ManyToManyField(to='timereg.Day', blank=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='monthly_report',
            field=models.ForeignKey(default=1, to='timereg.MonthlyReport'),
        ),
        migrations.AlterField(
            model_name='shiftdefault',
            name='possible_days',
            field=models.ManyToManyField(to='timereg.Day', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='monthlyreport',
            unique_together=set([('month', 'user')]),
        ),
    ]
