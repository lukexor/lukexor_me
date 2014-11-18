# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0005_auto_20141103_0719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
            ],
            options={
                'db_table': 'role',
                'verbose_name': 'role',
                'verbose_name_plural': 'roles',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='comment_count',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='project',
            name='client',
        ),
        migrations.RemoveField(
            model_name='project',
            name='role',
        ),
        migrations.AddField(
            model_name='article',
            name='authors',
            field=models.ManyToManyField(related_query_name=b'article', related_name=b'articles', db_table=b'article_author', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='note',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='website',
            field=models.CharField(max_length=2083, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='clients',
            field=models.ManyToManyField(related_query_name=b'client', related_name=b'client', db_table=b'project_client', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(related_query_name=b'roles', related_name=b'roles', db_table=b'project_role', to='lukexor_me.Role'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='website',
            field=models.CharField(max_length=2083, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(related_query_name=b'comment', related_name=b'comment', db_table=b'article_comment', to=b'lukexor_me.Comment'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_query_name=b'article', related_name=b'articles', db_table=b'article_tag', to=b'lukexor_me.Tag'),
        ),
        migrations.AlterField(
            model_name='article',
            name='time_to_read',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=45, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
        ),
    ]
