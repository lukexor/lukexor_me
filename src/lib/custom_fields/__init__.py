from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class UpdatedDateTimeField(models.DateTimeField):
    __metaclass__ = models.SubfieldBase
    description = "A DateTimeField used for an 'updated' column."

    def __init__(self, *args, **kwargs):
        super(UpdatedDateTimeField, self).__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "UpdatedDateTimeField"

    def pre_save(self, model_instance, add):
        return timezone.now()

class CreatedDateTimeField(models.DateTimeField):
    __metaclass__ = models.SubfieldBase
    description = "A DateTimeField used for a 'created' column."

    def __init__(self, *args, **kwargs):
        super(CreatedDateTimeField, self).__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CreatedDateTimeField"

    def pre_save(self, model_instance, add):
        if not model_instance.pk:
            return timezone.now()
        else:
            return model_instance.created.replace(tzinfo=timezone.utc)

