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


today = datetime.now().day

current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
#full time is the float value of the current hour
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def dash(request):
    allSessionData = Session_Data.objects.all()
    hwData = Hw_Data.objects.all()
    for session in allSessionData:
        session_day = session.finish_time.date().day
        session_hour = session.finish_time.hour - 7
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
    df = pd.DataFrame({"thickness in width": keys, "thickness in height": values})

    graphs = []

    fig = px.bar(df, x='thickness in width', y='thickness in height', title="how thick the got dang square be")
    plot_div = plot({'data': fig}, 
                     output_type='div')

    return render(request, 'Dashboard/page.html',
                context={'plot_div': plot_div})
