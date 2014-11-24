# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0003_auto_20141123_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_published',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
