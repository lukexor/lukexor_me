# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.sites.models import Site

def update_site(apps, schema_editor):
    site = Site.objects.get(pk=1)
    site.domain = 'lukexor.me'
    site.name = 'lukexor.me'
    site.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0010_auto_20141127_1211'),
    ]

    operations = [
        migrations.RunPython(update_site),
    ]
