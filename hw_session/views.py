from django.http import request
from django.views.decorators.csrf import csrf_protect 
from django.shortcuts import render, redirect
from .forms import Sessionform
from .canvas import Canvas_Cl

import calendar

START_TIME = None 

# Create your views here.
def home(request):
    if request.method == "POST":
        session_form = Sessionform(request.POST)
        if session_form.is_valid():
            session_form.save()
            print("Session form saved to DB")
        return redirect("/dashboard")

    canvas_cl = Canvas_Cl()
    hw_data = canvas_cl.refreshHwData()
    # hw_data = getHWData()

    for i in hw_data:
        print('---------------------------------------------')
        #Get the due date of the assignment to manipulate it
        reformed_datetime = str(i.due_date)
        # print(reformed_datetime)
        assignment = str(i.name)
        print(assignment)

        #Parse the due date
        if ' ' in reformed_datetime:
            reformed_datetime = reformed_datetime.split(' ')
        else:
            reformed_datetime = reformed_datetime.split('T')
        time_due_str = reformed_datetime[1]
        time_due_str1 = time_due_str.split(':')

        # To get the hour right 
        hour = (int(time_due_str1[0]) + 5) % 12
        if hour == 0:
            hours = 12
            hour_due_str = str(hours)
            
        else:
            hours = hour
            hour_due_str = str(hours)
        # time = datetime()
        time = (hour_due_str + ':' + time_due_str1[1])

        #Getting the Month and day of the year 
        date_due = reformed_datetime[0]
        date_due = date_due.split('-')
        parsed_year, parsed_month, parsed_day = int(date_due[0]), int(date_due[1]), (int(date_due[2])-1)
        # datetime_dueDate = datetime(parsed_year, parsed_month, parsed_day)
        # print(datetime_dueDate)

        dayNumber = calendar.weekday(parsed_year, parsed_month, parsed_day)
        days =["Mon", "Tue", "Wed", "Thu",
                            "Fri", "Sat", "Sun"]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # print(parsed_month)
        final_month = (months[parsed_month -1])
        final_day = (days[dayNumber])
        i.due_date = final_day
        print(str(i.due_date))

    context = {
        "hw_data" : hw_data,
        "session_form" : Sessionform()
    }
    return render(request, 'hw_session/index.html', context)

# def create_session(request):
#     return render(request, 'runningSession.html', context={})


# def update_start_time(request):
#     print("Triggered update_start_time")

#     if request.method == 'POST':
#         body = json.loads(request.body)
#         START_TIME = body 
#         print(body['min'])
#         return response.HttpResponse(f"Handled POST")
#     return response.HttpResponse(f"Handled ${request.method}")