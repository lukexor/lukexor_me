# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0002_auto_20141103_0613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleauthor',
            name='article_id',
        ),
        migrations.RemoveField(
            model_name='articleauthor',
            name='author',
        ),
        migrations.DeleteModel(
            name='ArticleAuthor',
        ),
        migrations.RemoveField(
            model_name='articlecategory',
            name='article_id',
        ),
        migrations.RemoveField(
            model_name='articlecategory',
            name='category_id',
        ),
        migrations.DeleteModel(
            name='ArticleCategory',
        ),
        migrations.RenameField(
            model_name='articlecomment',
            old_name='article_id',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='articlecomment',
            old_name='comment_id',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='articletag',
            old_name='article_id',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='articletag',
            old_name='tag_id',
            new_name='tag',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(related_query_name=b'article', related_name=b'articles', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='lukexor_me.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(related_query_name=b'article', related_name=b'articles', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
