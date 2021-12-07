from django.db import models
from django.db.models.deletion import CASCADE

INTERVAL_CHOICES =  [
    (.05, "3mins"),
    ( .25, "15mins"),
    ( .5, "30mins"),
    ( .75, "45mins"),
    ( 1, "1hr"),
    ( 1.25, "1hr 15mins"),
    ( 1.5, "1hr 30mins")
]

class Session_Data(models.Model):
    """A model (database) that contains all of the current homework session data. A homework session begins 
    when they click start on the home page.
    """
    goal = models.CharField(max_length=100)
    time_limit_hours = models.IntegerField(null=True)
    time_limit_mins = models.IntegerField(null=True)
    # selected_assignments = models.JSONField(null=True)
    start_time = models.CharField(max_length=200, null=True)
    # finish_time = models.CharField(max_length = 200, null =True)
    # finish_time = models.DateTimeField(auto_now_add=True, null=True)
    finish_time = models.DateTimeField(null=True)
    break_interval = models.FloatField(max_length=30, choices=INTERVAL_CHOICES, default=.05, null=True)
    goal_accomplished = models.BooleanField(null=True)
    selected_assignment_count = models.IntegerField(null=True)
    completed_count = models.IntegerField(null=True)
    def __str__(self):
        """A method to get the goal from the database.

        Returns:
            String : the goal the user input for their session.
        """
        return self.goal
    
# Create your models here.
class Hw_Data(models.Model):
    """A model (database) for all of the users homework data populated using the Canvas API.
    """
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=100)
    is_selected = models.BooleanField(null=True)
    is_completed = models.BooleanField(null=True)
    loaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        """A method to get the assignment name from the database.

        Returns:
            String : the assignment name form the database
        """
        return self.name

