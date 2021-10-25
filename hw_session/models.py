from django.db import models
import json
from canvasapi import Canvas
import threading

# Create your models here.
class hw_data(models):
    name = models.CharField(max_length=30)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=30)
    completed = models.BooleanField()

class session_data(models):
    goal = models.CharField()
    time_limit = models.FloatField()
    selected_assignments = models.JSONField()
    start_time = models.DateTimeField()