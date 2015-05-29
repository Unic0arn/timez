# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timereg', '0004_auto_20150511_0314'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('month', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='shift',
            name='worker',
        ),
        migrations.RemoveField(
            model_name='shiftfragment',
            name='worker',
        ),
        migrations.AddField(
            model_name='shift',
            name='monthly_report',
            field=models.ForeignKey(to='timereg.MonthlyReport', default=0),
        ),
    ]
