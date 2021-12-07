from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
from .dataSanitize import *

def dash(request):

    graphable = sanitize()

    #Fig1 = bar plot of time Spent Working in minutes each day"
    fig1 = px.bar(graphable, x='date_day', y='time_spent_mins',
                             labels={'date_day':'Day','time_spent_mins': 'Time Spent Working (min)'})                       
    fig1.update_xaxes(dtick=1)
    time_spent_each_day = plot({'data': fig1}, output_type='div')

    #Fig2 = scatter plot of percentage of goal met each day with integrated duration
    fig2 = px.scatter(graphable, x='date_day', y='time_goal_met',
                                color = 'time_spent_mins',
                                size='size',
                                labels={'date_day': 'Day', 'time_goal_met': 'Goal Acheived (%)','time_spent_mins':'Min Spent'})
    fig2.update_xaxes(dtick=1)
    goals_met_each_day = plot({'data': fig2}, output_type='div')

    #Fig3 = bar chart of percentage of selected assignments completed
    fig3 = px.bar(graphable, x='date_day', y='assignment_goal_met',
                                labels={'date_day': 'Day', 'assignment_goal_met': 'Assignment Goal Met'})
    fig3.update_xaxes(dtick=1)
    assignment_goals_met = plot({'data': fig3}, output_type='div')
    #https://plotly.com/python/reference/layout/xaxis/ for limiting the range

    #Fig4 = heatmap showing productivity
    fig4 = px.density_heatmap(graphable, x='date_day',y='start_time_hours',z='assignment_goal_met',
                                nbinsy=10, nbinsx=5,
                                labels={'date_day': 'Day','start_time_hours': 'Time of Day', 'assignment_goal_met': 'Productivity'})
    fig4.update_yaxes(dtick=1)
    fig4.update_xaxes(dtick=1)
    productivity_density = plot({'data': fig4}, output_type='div')

    context={'time_spent_each_day': time_spent_each_day,
            'goals_met_each_day': goals_met_each_day,
            'assignment_goals_met': assignment_goals_met,
            'productivity': productivity_density}


    return render(request, 'Dashboard/page.html', context)
    
    
