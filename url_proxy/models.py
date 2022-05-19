from django.db import models


class UrlProxy(models.Model):
    SHORT_URL_BASE = 'http://localhost:8000/'

    original = models.URLField(max_length=256, unique=True)
    short = models.URLField(max_length=50, unique=True)
