from django import forms
from . import models

# class DataForm(forms.ModelForm):
#     class Meta:
#         model = models.Hw_Data
#         fields = ['name','due_date','course','submitted','hw_session']

# class Sessionform(forms.ModelForm):
#     class Meta:
#         model = models.Session_Data
#         fields = ['goal','time_limit_hours','time_limit_mins','break_interval']    
        

class Sessionform(forms.ModelForm):
    class Meta:
        model = models.Session_Data
        fields = ['goal','time_limit_hours','time_limit_mins','break_interval', 'start_time'] 