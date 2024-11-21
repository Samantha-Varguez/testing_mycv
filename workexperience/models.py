from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Create your models here.
class WorkExperience(models.Model):
    position     = models.TextField(default='')
    company = models.TextField(default='')
    location = models.TextField(default='')
    description = models.TextField(default='')
    start_date = models.DateTimeField(default=now, blank=True)
    end_date   = models.DateTimeField(default=now, blank=True)
    posted_by  = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
