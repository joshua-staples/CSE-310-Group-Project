from django.db import models
import sqlite3
from django import forms


from django.db.models.deletion import CASCADE

INTERVAL_CHOICES =  [
    ( .25, "15mins"),
    ( .5, "30mins"),
    ( .75, "45mins"),
    ( 1, "1hr"),
    ( 1.25, "1hr 15mins"),
    ( 1.5, "1hr 30mins")
]

class Session_Data(models.Model):
    goal = models.CharField(max_length=100)
    time_limit_hours = models.IntegerField(null=True)
    time_limit_mins = models.IntegerField(null=True)
    selected_assignments = models.JSONField(null=True)
    # start_time = models.JSONField(null=True)
    start_time = models.CharField(max_length=200, null=True)
    finish_time = models.DateTimeField(auto_now_add=True, null=True)
    break_interval = models.FloatField(max_length=30, choices=INTERVAL_CHOICES, default=.75, null=True)
    goal_accomplished = models.BooleanField(null=True)
    completed_count = models.IntegerField(null=True)
    def __str__(self):
        return self.goal
    
# Create your models here.
class Hw_Data(models.Model):
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=100)
    is_selected = models.BooleanField(null=True)
    is_completed = models.BooleanField(null=True)
    loaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

