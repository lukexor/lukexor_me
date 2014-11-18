# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0008_auto_20141114_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gravatar',
            field=models.CharField(max_length=2083, null=True, blank=True),
            preserve_default=True,
        ),
    ]
