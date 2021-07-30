# -*- coding: utf-8 -*-
from django.db import models


class Thing(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    data = models.JSONField(null=True, default=None, blank=True)


class RelatedThing(models.Model):
    thing = models.ForeignKey(Thing, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    data = models.JSONField(null=True, default=None, blank=True)
