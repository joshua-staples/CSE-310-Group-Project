from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime
import plotly.express as px
import pandas as pd
import json

today = datetime.now().day

current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
#full time is the float value of the current hour
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def dash(request):
  
    ## GETTING THE CURRENT TIME AND SETTING UP THE INITIAL DB

    finish_time_mins = []
    finish_time_hours = []
    finish_time_days = []
    finish_times = []

    start_time_mins = []
    start_time_hours = []
    start_time_days = []
    start_times = []



    session_data = pd.DataFrame(list(Session_Data.objects.all().values()))
    # print(session_data.columns)

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

    for time in session_data['start_time']:
        # print(session_data['start_time'])
        # print(time,'------')
        # print(type(time),'------------------------')

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
        
    #days
    session_data['date_day'] = finish_time_days
    #finish time
    session_data['fin_time_hour'] = finish_time_hours
    session_data['fin_time_minutes'] = finish_time_mins
    session_data['finish_times'] = finish_times
    #start time
    session_data['start_time_hours'] = start_time_hours
    session_data['start_time_minutes'] = start_time_mins
    session_data['start_times'] = start_times
    #finish time - start time
    session_data['time_spent'] = session_data['finish_times'] - session_data['start_times']



    # GET GOAL TIMES AND OVERLAY IT
    session_data["time_limit_mins"] = session_data["time_limit_mins"]/60
    session_data["time_goal"] = session_data['time_limit_hours'] + session_data['time_limit_mins']
    session_data["goal_met"] =  (session_data['time_spent'] / session_data['time_goal']) * 100

    #GRAPHING THE TIME SPENT EACH DAY

    graphable = session_data
    graphable['time_spent'] = round(graphable['time_spent'] * 60)
    

    fig2 = px.bar(graphable, x='date_day', y='time_spent', labels={'date_day': 'Day',
                             'time_spent': 'Time Spent Working (min)', 'goal_met':'Goal Acheived (%)'})                       
    time_spent_each_day = plot({'data': fig2}, output_type='div')

    # context = {'time_spent_each_day': time_spent_each_day}

    # return render(request, 'Dashboard/page.html', context)

    fig1 = px.scatter(graphable, x='date_day', y='goal_met', size = 'time_spent', labels={'date_day': 'Day', 'goal_met': 'Goal Met (%)', 'time_spent': 'Time Spent Working'})

    goals_met_each_day = plot({'data': fig1}, output_type='div')
    
    

    context={'time_spent_each_day': time_spent_each_day,
            'goals_met_each_day': goals_met_each_day}

    # fig2 = px.scatter(session_data, x = 'date_day', y = 'time_goal', labels={'date_day': 'Day', 'time_goal': 'Time Goal'})
    # goals_met_each_day = plot({'data':fig2}, output_type='div')

    # context = {'goals_met_each_day': goals_met_each_day}
                             
    # context={'time_spent_each_day': time_spent_each_day,
    #         'goals_met_each_day': goals_met_each_day}

    return render(request, 'Dashboard/page.html', context)
    
    
    """End Pass"""

    # fin1 = []
    # hr1 = []
    # min1 = []
    # data_quick = pd.DataFrame(list(Session_Data.objects.all().values()))
    # # print(data_quick)
    # for time in data_quick['finish_time']:
    #     mins = time.minute
    #     mins = mins/60
    #     # print(mins)
    #     min1.append(mins)
    #     fin2 = time.date().day
    #     hr2 = time.hour - 7
    #     if hr2 < 0:
    #         hr2 = 24 + hr2
    #         fin2 = fin2 - 1
    #     fin1.append(fin2)
    #     hr1.append(hr2)
    # data_quick['date_day'] = fin1
    # data_quick['fin_hour'] = hr1
    # data_quick['fin_mins'] = min1
    # float_time = data_quick['fin_hour'] + data_quick['fin_mins']
    # data_quick['float_time'] = float_time
    # # print(data_quick['float_time'])
    # # print(data_quick.columns)

    # time_df = pd.DataFrame(data_quick, columns = ['id','date_day','fin_hour','break_interval','time_limit_mins','time_limit_hours'])

    # graphs = []
    # fig = px.bar(time_df, x='date_day', y='fin_hour', title="how thick the got dang square be",
    #                 color='fin_hour')
    # plot_div = plot({'data': fig}, 
    #                  output_type='div')

    # return render(request, 'Dashboard/page.html',
    #             context={'plot_div': plot_div})
