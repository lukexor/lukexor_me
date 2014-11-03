# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0004_auto_20141103_0654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecomment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articlecomment',
            name='comment',
        ),
        migrations.DeleteModel(
            name='ArticleComment',
        ),
        migrations.RemoveField(
            model_name='articletag',
            name='article',
        ),
        migrations.RemoveField(
            model_name='articletag',
            name='tag',
        ),
        migrations.DeleteModel(
            name='ArticleTag',
        ),
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(to='lukexor_me.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='lukexor_me.Tag'),
            preserve_default=True,
        ),
    ]
