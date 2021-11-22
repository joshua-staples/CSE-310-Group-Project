from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import hw_session
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime
import plotly.express as px
from plotly.graph_objs import Scatter
from plotly.offline import plot
import pandas as pd

# Generating some data for plots.
y1 = {}

# upcoming_assignments = []
assignments_worked_on = []
assignments_completed = []

days_success = {}

#time spent today compared to goal
#assignments completed
#weekly work
# parsing the current time 
today = datetime.now().day

current_hour = str(datetime.now().hour)
current_mins = str(datetime.now().minute)
#full time is the float value of the current hour
full_time = round(int(current_hour) + (int(current_mins)/60),2)

def dash(request):
    print('--------------------------------------------')
    print(today)

    allSessionData = Session_Data.objects.all()
    hwData = Hw_Data.objects.all()
    for session in allSessionData:
        session_day = session.finish_time.date().day
        print(session_day)
        #Try and fix this time zone error later
        session_hour = session.finish_time.hour - 7
        print(session_day)
        if session_day in range(today - 6, today+1):
            if not str(session_day) in y1:
                y1[str(session_day)] = session_hour
               
            else:
                y1[str(session_day)] = y1[str(session_day)] + session_hour

            
                
            # y1[session_day] = session_hour
            # print("H:", session_hour)
            # print(session_day)
            # days_success[session_day] = session.start_time, hwData.loaded_at
    print("y1: ", y1)  
        # for finding work done today make a comparison between start time values and current date time values to only show 
        # put a map in for lookup effeciency 
        # Need to add a button to count completed assignments and make a comparison between assignments_total and assignments_completed then print remainder
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    


    # List of graph objects for figure.
    # Each object will contain on series of data.

    # x = [i for i in list(y1.keys)]
    # y2 = [i for i in list(y1.values)]
    df = pd.DataFrame(y1)

    key = list(y1.keys())
    value = list(y1.values())
    print(key)
    print(value)
    x = [i for i in key]
    y2 = [i for i in value]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    # graphs = []

    # #Bar graph
    # # bar = px.bar(days_success, x='day', y = '')

    
    plot_div = plot(bar([df]), output_type = 'div')
    # # Adding linear plot of y1 vs. x.
    # graphs.append(
    #     px.bar(x=x, y=y2, 'type':'bar')
    # )

    # Setting layout of the figure.
    layout = {
        'title': 'Time Goal',
        'xaxis_title': 'Days',
        'yaxis_title': 'Goal Completed'
    }

    # plot_div = plot([box(x=x, y=y2, mode='bar', name='tets')])

    # Getting HTML needed to render the plot.
    # plot_div = plot({'data': graphs, 'layout': layout}, 
    #                 output_type='div')
    # plot_div = plot([Scatter(x=x, y=y2,
    #                     mode='lines', name='test',
    #                     opacity=0.8, marker_color='green')],
    #            output_type='div')

    return render(request, 'Dashboard/page.html',
                  context={'plot_div': plot_div})
