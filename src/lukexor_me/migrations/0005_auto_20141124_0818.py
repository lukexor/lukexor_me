# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0004_auto_20141124_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(blank=True, to='lukexor_me.Project', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(blank=True, to='lukexor_me.Article', null=True),
        ),
    ]
