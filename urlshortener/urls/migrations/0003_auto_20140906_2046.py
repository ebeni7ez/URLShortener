# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0002_auto_20140906_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='date_submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
