from django import forms
from . import models        

#Creates a HTML form for the models. 
class Sessionform(forms.ModelForm):
    class Meta:
        model = models.Session_Data
        fields = ['goal','time_limit_hours','time_limit_mins','break_interval', 'start_time', 'selected_assignment_count', 'completed_count'] 