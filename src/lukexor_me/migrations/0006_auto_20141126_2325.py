# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0005_auto_20141124_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(serialize=False, primary_key=True)),
                ('cc_author_name', models.CharField(max_length=90)),
                ('cc_title', models.CharField(max_length=255)),
                ('cc_image_url', models.CharField(max_length=2083)),
                ('filename', models.CharField(unique=True, max_length=255)),
                ('width', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='project',
            old_name='description',
            new_name='body',
        ),
        migrations.AddField(
            model_name='article',
            name='photos',
            field=models.ManyToManyField(to='lukexor_me.Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='date_published',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='is_published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='photos',
            field=models.ManyToManyField(to='lukexor_me.Image', blank=True),
            preserve_default=True,
        ),
    ]
