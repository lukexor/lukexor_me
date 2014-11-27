# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0006_auto_20141126_2325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='article',
            name='photos',
        ),
        migrations.RemoveField(
            model_name='project',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='project',
            name='photos',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
