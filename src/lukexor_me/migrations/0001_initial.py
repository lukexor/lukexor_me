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
                ('first_name', models.CharField(max_length=45, blank=True)),
                ('last_name', models.CharField(max_length=45, blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'joined on')),
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
                ('title', models.CharField(max_length=255)),
                ('permalink_title', models.CharField(unique=True, max_length=45)),
                ('body', models.TextField(blank=True)),
                ('time_to_read', models.CharField(max_length=30, blank=True)),
                ('comment_count', models.PositiveIntegerField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article',
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('article_author_id', models.AutoField(serialize=False, primary_key=True)),
                ('article_id', models.ForeignKey(to='lukexor_me.Article')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'article_author',
                'verbose_name': 'article authors',
                'verbose_name_plural': 'article authors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('article_category_id', models.AutoField(serialize=False, primary_key=True)),
                ('article_id', models.ForeignKey(to='lukexor_me.Article')),
            ],
            options={
                'db_table': 'article_category',
                'verbose_name': 'article category',
                'verbose_name_plural': 'article categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('article_comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('article_id', models.ForeignKey(to='lukexor_me.Article')),
            ],
            options={
                'db_table': 'article_comment',
                'verbose_name': 'article comment',
                'verbose_name_plural': 'article comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('article_tag_id', models.AutoField(serialize=False, primary_key=True)),
                ('article_id', models.ForeignKey(to='lukexor_me.Article')),
            ],
            options={
                'db_table': 'article_tag',
                'verbose_name': 'article tag',
                'verbose_name_plural': 'article tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
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
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
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
                ('title', models.CharField(max_length=255)),
                ('permalink_title', models.CharField(unique=True, max_length=45)),
                ('description', models.TextField(blank=True)),
                ('role', models.CharField(max_length=45, blank=True)),
                ('client', models.CharField(max_length=80, blank=True)),
                ('date_started', models.DateTimeField(null=True, verbose_name=b'started on', blank=True)),
                ('date_completed', models.DateTimeField(null=True, verbose_name=b'completed on', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'project',
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tag',
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='articletag',
            name='tag_id',
            field=models.ForeignKey(to='lukexor_me.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='comment_id',
            field=models.ForeignKey(to='lukexor_me.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecategory',
            name='category_id',
            field=models.ForeignKey(to='lukexor_me.Category'),
            preserve_default=True,
        ),
    ]
