from django.db import models

class BrState(models.Model):
    state = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    notifier = models.CharField(max_length=1000, default=[{}])
    