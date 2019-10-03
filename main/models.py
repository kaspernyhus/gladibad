from django.db import models

class BrState(models.Model):
    state = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
<<<<<<< HEAD
    notifier = models.CharField(max_length=1000, default=[{}])
=======
    notifier = models.IntegerField(default=0)
>>>>>>> 4d7551e1fdc51ffe55d60c2ff82d3657d6da0c69
