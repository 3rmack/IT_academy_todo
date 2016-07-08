from __future__ import unicode_literals
from django.db import models


class Tasks(models.Model):
    task = models.CharField(max_length=100)
    status = models.BooleanField(auto_created=True, default=False)
    order = models.IntegerField()
