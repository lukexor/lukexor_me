# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def combine_names(apps, schema_editor):
    CustomUser = apps.get_model("lukexor_me", "CustomUser")

    for user in CustomUser.objects.all():
        user.full_name = "%s %s" % (user.first_name, user.last_name)
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lukexor_me', '0009_auto_20141127_1231'),
    ]

    operations = [
        migrations.RunPython(combine_names),
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]
