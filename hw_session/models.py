from django.db import models
import json
from canvasapi import Canvas
import threading

# Create your models here.
class Hw_Data(models.Model):
    name = models.CharField(max_length=30)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=30)
    submitted = models.BooleanField()

class Session_Data(models.Model):
    goal = models.CharField(max_length=30)
    time_limit = models.FloatField()
    selected_assignments = models.JSONField()
    start_time = models.DateTimeField()