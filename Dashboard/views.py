from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime
import plotly.express as px
import pandas as pd
import json


# Getting the current time 
today = datetime.now().day
current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def dash(request):
  
    #Setting up the dataframe we are going to use

    finish_time_mins = []
    finish_time_hours = []
    finish_time_days = []
    finish_times = []

    start_time_mins = []
    start_time_hours = []
    start_time_days = []
    start_times = []


    

    session_data = pd.DataFrame(list(Session_Data.objects.all().values()))

    #Get the time the hw session ended

    for time in session_data['finish_time']:
        fin_min = time.minute
        fin_min = fin_min/60 
        fin_day = time.date().day
        fin_hour = time.hour - 7
        if fin_hour < 0:
            fin_hour = 24 + fin_hour
            fin_day = fin_day - 1
        float_fin_time = fin_hour + fin_min
        finish_time_mins.append(fin_min)
        finish_time_hours.append(fin_hour)
        finish_time_days.append(fin_day)
        finish_times.append(float_fin_time)

    #Get the time the hw session started

    for time in session_data['start_time']:

        json_start_time = json.loads(time)
        start_day = json_start_time['day']
        start_hour = json_start_time['hour']
        start_min = json_start_time['min']

        start_min = start_min/60
        float_start_time = start_hour + start_min

        start_time_days.append(start_day)
        start_time_hours.append(start_hour)
        start_time_mins.append(start_min)
        start_times.append(float_start_time)
        
    #Add the comparison data between the start time and finish time to the session_data df
    session_data['date_day'] = finish_time_days
    session_data['fin_time_hour'] = finish_time_hours
    session_data['fin_time_minutes'] = finish_time_mins
    session_data['finish_times'] = finish_times
    session_data['start_time_hours'] = start_time_hours
    session_data['start_time_minutes'] = start_time_mins
    session_data['start_times'] = start_times
    session_data['time_spent'] = session_data['finish_times'] - session_data['start_times']
    session_data["time_limit_mins"] = session_data["time_limit_mins"]/60
    session_data["time_goal"] = session_data['time_limit_hours'] + session_data['time_limit_mins']
    session_data["goal_met"] =  (session_data['time_spent'] / session_data['time_goal']) * 100
    

    """Graphing"""


    #Creating another instance of the hw session dataframe for graphing purposes
    graphable = session_data
    graphable['time_spent_mins'] = round(graphable['time_spent'] * 60)
    #Altering some aspects of the new dataframe for graphing purposes 
    for i in graphable['goal_met']:
        if i > 100:
            i = 100
        else:
            pass
    
    #Creating our bar graph "Time Spent Working in Minutes Each Day"
    fig1 = px.bar(graphable, x='date_day', y='time_spent_mins',
                             labels={'time_spent_mins': 'Time Spent Working (min)', 'goal_met':'Session Time Used (%)', '':''})                       
    time_spent_each_day = plot({'data': fig1}, output_type='div')

    #Creating our scatter plot "Percentage of Goal Met Each Day" with integrated duration
    fig2 = px.scatter(graphable, x='date_day', y='goal_met',
                                 size = 'time_spent_mins',
                                labels={'time_spent':'Time Spent in Hours','date_day': 'Day', 'goal_met': 'Goal Acheived (%)', 'time_spent': 'Time Spent Working (min)'})
    goals_met_each_day = plot({'data': fig2}, output_type='div')

    # fig3 = 
    
    

    context={'time_spent_each_day': time_spent_each_day,
            'goals_met_each_day': goals_met_each_day}


    return render(request, 'Dashboard/page.html', context)
    
    
