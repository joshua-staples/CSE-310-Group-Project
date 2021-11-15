# from django.shortcuts import render
# from plotly.offline import plot
# from plotly.graph_objs import Scatter
# import plotly.graph_objects as go

# def dash(request):
#     x_data = [0,1,2,3]
#     y_data = [x**2 for x in x_data]

#     lt = {
#         'Title': 'Random Graph',
#         'xaxis_title': 'X',
#         'yaxis-title:': 'Y',
#         'height': '70vh',
#         'width': '50vh'
#     }

#     plot_div = plot([Scatter(x=x_data, y=y_data,
#                         mode='lines', name='test',
#                         opacity=0.8, marker_color='green')],
#                         layout = lt,
#                output_type='div')


#     return render(request, "Dashboard/page.html", context={'plot_div': plot_div})

from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import hw_session
from hw_session.models import Hw_Data, Session_Data
from datetime import datetime



# upcoming_assignments = []
assignments_worked_on = []
assignments_completed = []

# days_success = {}


def dash(request):
    # parsing the current time 
    today = str(datetime.now().day)
    today = int(today)
    current_hour = str(datetime.now())
    time_space = current_hour.split(' ')
    time_time = time_space[1]
    current_time = time_time.split(':')
    hour = current_time[0]
    minutes = current_time[1]
    min_to_hour = round((int(minutes)/60),2)
    full_time = int(hour) + min_to_hour
    
    allSessionData = Session_Data.objects.all()
    hwData = Hw_Data.objects.all()
    print('-----------------------------------')
    for session in allSessionData:
        # parsing the session start time string
        session_day = str(session.start_time.date())
        split_day = session_day.split('-')
        day = split_day[2]
        day = int(day)
        if day == today:
            print(full_time)
            print('---------------------')
            print(session.time_limit_hours, session.time_limit_mins)
            print('---------------------')
            start_time = (int(session.start_time.time().hour)-7) + (int(session.start_time.time().minute)/60) 
            print(start_time)
            


        # print(tab_split)
        
        

        # for finding work done today make a comparison between start time values and current date time values to only show 
        # put a map in for lookup effeciency 
        # Need to add a button to count completed assignments and make a comparison between assignments_total and assignments_completed then print remainder
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    
    # Generating some data for plots.
    x = [i for i in range(-10, 11)]
    y1 = [3*i for i in x]
    y2 = [i**2 for i in x]
    y3 = [10*abs(i) for i in x]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Adding scatter plot of y2 vs. x. 
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8, 
                   marker_size=y2, name='Scatter y2')
    )

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y'
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    return render(request, 'Dashboard/page.html',
                  context={'plot_div': plot_div})
