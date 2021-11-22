from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import hw_session
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime
import plotly.express as px





# upcoming_assignments = []
assignments_worked_on = []
assignments_completed = []

days_success = {}

#time spent today compared to goal
#assignments completed
#weekly work

def dash(request):
    # parsing the current time 
    today = str(datetime.now().day)
    today = int(today)
    print(today)
    current_hour = str(datetime.now().hour)
    print(current_hour)

    # time_space = current_hour.split(' ')
    # time_time = time_space[1]
    # current_time = time_time.split(':')
    # hour = current_time[0]
    # minutes = current_time[1]
    # min_to_hour = round((int(minutes)/60),2)
    #full time is the current time
    # full_time = int(hour) + min_to_hour
    
    allSessionData = Session_Data.objects.all()
    hwData = Hw_Data.objects.all()
    # print('-----------------------------------')
    for session in allSessionData:
        # parsing the session start time string to compare it to the 
        session_day = str(session.start_time.date())
        split_day = session_day.split('-')
        day = split_day[2]
        day = int(day)
        if day in range (today - 6, today):
            print("yes")
            days_success[day] = session.start_time, hwData.loaded_at
            print(days_success)
            # print(day)
        
        # for finding work done today make a comparison between start time values and current date time values to only show 
        # put a map in for lookup effeciency 
        # Need to add a button to count completed assignments and make a comparison between assignments_total and assignments_completed then print remainder
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    
    # Generating some data for plots.
    x = [i for i in range(0, 1)]
    y1 = [3*i for i in x]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Time Goal',
        'xaxis_title': 'Days',
        'yaxis_title': 'Goal Completed'
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    return render(request, 'Dashboard/page.html',
                  context={'plot_div': plot_div})
