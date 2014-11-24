# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0002_auto_20141121_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to=b'lukexor_me.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(to=b'lukexor_me.Role'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to=b'lukexor_me.Tag', blank=True),
        ),
    ]
