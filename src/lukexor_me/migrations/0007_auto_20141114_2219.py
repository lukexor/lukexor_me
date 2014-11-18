# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0006_auto_20141114_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='time_to_read',
        ),
        migrations.AddField(
            model_name='article',
            name='minutes_to_read',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(related_query_name=b'article', related_name=b'articles', to='lukexor_me.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(related_query_name=b'comment', related_name=b'comment', db_table=b'article_comment', to=b'lukexor_me.Comment', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date published'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_query_name=b'article', related_name=b'articles', db_table=b'article_tag', to=b'lukexor_me.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date posted'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added'),
        ),
        migrations.AlterField(
            model_name='project',
            name='clients',
            field=models.ManyToManyField(related_query_name=b'client', related_name=b'client', db_table=b'project_client', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added'),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_completed',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_started',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
