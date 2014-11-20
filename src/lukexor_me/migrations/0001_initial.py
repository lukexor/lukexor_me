# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45, null=True, blank=True)),
                ('website', models.CharField(max_length=2083, null=True, blank=True)),
                ('gravatar', models.CharField(max_length=2083, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('permalink_title', models.CharField(unique=True, max_length=45)),
                ('summary', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('minutes_to_read', models.PositiveIntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date published')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('authors', models.ManyToManyField(related_query_name=b'article', related_name=b'articles', db_table=b'article_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article',
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
            ],
            options={
                'db_table': 'category',
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date posted')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('permalink_title', models.CharField(unique=True, max_length=45)),
                ('summary', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('website', models.CharField(max_length=2083, null=True, blank=True)),
                ('date_started', models.DateTimeField(null=True, blank=True)),
                ('date_completed', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
                ('clients', models.ManyToManyField(related_query_name=b'client', related_name=b'client', db_table=b'project_client', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'db_table': 'project',
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
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
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, auto_now=True)),
            ],
            options={
                'db_table': 'tag',
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='roles',
            field=models.ManyToManyField(related_query_name=b'roles', related_name=b'roles', db_table=b'project_role', to='lukexor_me.Role'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(related_query_name=b'article', related_name=b'articles', to='lukexor_me.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(related_query_name=b'comment', related_name=b'comment', db_table=b'article_comment', to='lukexor_me.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_query_name=b'article', related_name=b'articles', db_table=b'article_tag', to='lukexor_me.Tag', blank=True),
            preserve_default=True,
        ),
    ]
