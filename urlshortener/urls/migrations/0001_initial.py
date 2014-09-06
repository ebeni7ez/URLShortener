# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('word', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('used', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('word', models.OneToOneField(primary_key=True, serialize=False, to='urls.Word')),
                ('url', models.URLField()),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'date_submitted',
            },
            bases=(models.Model,),
        ),
    ]
