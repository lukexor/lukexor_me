# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_published',
        ),
        migrations.AddField(
            model_name='article',
            name='date_published',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='date_published',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
