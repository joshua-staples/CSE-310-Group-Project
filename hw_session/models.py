from django.db import models


# Create your models here.
class Hw_Data(models.Model):
    name = models.CharField(max_length=30)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=30)
    submitted = models.BooleanField()

    def __str__(self):
        return self.name

class Session_Data(models.Model):
    goal = models.CharField(max_length=30)
    time_limit = models.FloatField()
    selected_assignments = models.JSONField()
    start_time = models.DateTimeField()