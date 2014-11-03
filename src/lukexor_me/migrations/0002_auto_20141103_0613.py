# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articleauthor',
            old_name='user_id',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='comment_count',
            field=models.PositiveIntegerField(default=0, verbose_name=b'# of comments'),
        ),
    ]
