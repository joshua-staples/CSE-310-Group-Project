from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import hw_session
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime
import plotly.express as px
from plotly.graph_objs import Scatter
import pandas as pd




y1 = {}
days = []
hours = []
fin1 = []
hr1 = []


today = datetime.now().day

current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
#full time is the float value of the current hour
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def dash(request):
    """Fast pass"""

    # data_quick = pd.DataFrame(list(Session_Data.objects.all().values()))
    # for time in data_quick['finish_time']:
    #     fin2 = time.date().day
    #     hr2 = time.hour - 7
    #     if hr2 < 0:
    #         hr2 = 24 - hr2
    #         fin2 = fin2 - 1
    #     fin1.append(fin2)
    #     hr1.append(hr2)
    # print(fin1, hr1)
    # data_quick['date_day'] = fin1
    # data_quick['fin_hour'] = hr1
    # print(data_quick.columns)
    # time_df = pd.DataFrame(data_quick, columns = ['id','date_day','fin_hour','break_interval','time_limit_mins','time_limit_hours'])
    # time_df = time_df.groupby(by='date_day').sum()
    # print(time_df)

    """End Fast pass"""

    allSessionData = Session_Data.objects.all()
    for session in allSessionData:
        session_day = session.finish_time.date().day
        # A bunch of adjustments to properly allign the time zone.
        session_hour = session.finish_time.hour - 7
        if session_hour < 0:
            session_hour = 24 + session_hour
            session_day = session_day - 1
        # Adding our values to the dictionary
        if session_day in range(today - 6, today+1):
            if not str(session_day) in y1:
                y1[str(session_day)] = session_hour
            else:
                y1[str(session_day)] = y1[str(session_day)] + session_hour 

    #list of keys and values            
    keys = list(y1.keys())
    values = list(y1.values())
    for i in keys:
        i = str(i)
    df = pd.DataFrame({"the wide thick": keys, "the tall thick": values})

    graphs = []

    fig = px.bar(df, x='the wide thick', y='the tall thick', title="how thick the got dang square be")
    plot_div = plot({'data': fig}, 
                     output_type='div')

    return render(request, 'Dashboard/page.html',
                context={'plot_div': plot_div})
