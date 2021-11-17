from django.http import request
from django.shortcuts import render, redirect
from .models import Hw_Data, Session_Data
from .forms import Sessionform
from canvasapi import Canvas
import threading
import json
import random
from datetime import datetime


#------------------------------------------------------------------------------
# Gets all of the assignments for a given course
#------------------------------------------------------------------------------
def getCourseAssignments(course, results, lock):
    assignmentList = []
    results[course.id] = {
        "courseName": '',
        "assignments": []
        }
    
    # Get all upcoming assignments from canvas
    assignments = course.get_assignments(bucket='upcoming')

    # Loop through and populate assignmentList with data
    for assignment in assignments:
        assignmentList.append({
            "name" : assignment.name,
            "due_date" : assignment.due_at,
            "course" : course.name,
            "submitted" : assignment.has_submitted_submissions
        })

    # Any time we modify shared results obj use lock for protection
    with lock:
        results[course.id]['courseName'] = course.name
        # We only want the assignments that haven't been submitted yet
        results[course.id]['assignments'] = list(filter(lambda a: a['submitted'] == False, assignmentList))


#------------------------------------------------------------------------------
# Starts a thread for each course to get its assignments.
# The assignments are put into the results object as the threads
# rejoin the main thread. The results object is then returned.
# A lock is used to protect the results obj from race conditions.
#------------------------------------------------------------------------------
def getAllAssignments(courses):
    courseThreads = []
    results = {}
    lock = threading.Lock()

    # Create a thread for each course
    for course in courses:
        thread = threading.Thread(target=getCourseAssignments, args=(course, results, lock))
        courseThreads.append(thread)

    # Start each thread
    for thread in courseThreads:
        thread.start()

    # Wait for each thread to complete
    for thread in courseThreads:
        thread.join()

    return results


#------------------------------------------------------------------------------
# gets all hwdata and creates instances of Hw_Data data model class
#------------------------------------------------------------------------------
def getHWData():
    with open('./hw_session/static/accessToken.json') as file:
        # Get the user info from accessToken file
        userInfo = json.load(file)

    # Set up the canvas object
    API_URL = "https://byui.instructure.com"
    API_KEY = userInfo["token"]
    canvas = Canvas(API_URL, API_KEY)

    # Get the user from canvas object
    myUserID = userInfo["user_id"]
    user = canvas.get_user(myUserID)
    print(f"Getting {user.name}'s information...")


    # Gets all courses that the user is actively enrolled in
    courses = user.get_courses(enrollment_state="active")

    # Get all of the upcoming unsubmitted assignments for the user
    results = getAllAssignments(courses)
    tasks = []

    for course in results:
        for assignment in results[course]['assignments']:
            hw = Hw_Data(
                name=assignment['name'], 
                due_date=assignment['due_date'], 
                course=assignment['course'], 
                submitted=assignment['submitted'],
                )
            print('hw:', hw)
            hw.save()
            tasks.append(hw)
    return tasks


def refreshHwData():
    tasks = []
    hourOfReload = 0
    curHour = (datetime.now().hour % 12)
    print("curHour: ", curHour)
    allHwData = Hw_Data.objects.all()
    for assignment in allHwData:
        tasks.append(assignment)
        dateTimeOfReload = assignment.loaded_at
        hourOfReload = (dateTimeOfReload.hour + 5 % 12)
        print("hourOfReload: ", hourOfReload)
    
    if curHour == hourOfReload:
        print("No need to reload")
        return tasks
    else:
        print("Reloaded Data")
        Hw_Data.objects.all().delete()
        return getHWData()

# Create your views here.
def home(request):
    if request.method == "POST":
        session_form = Sessionform(request.POST)
        if session_form.is_valid():
            session_form.save()
            print("Session form saved to DB")
        return redirect("/dashboard")
    #here

    hw_data = refreshHwData()
    for i in hw_data:
        reformed_datetime = i.due_date

        # reformed_datetime = reformed_datetime.split('T')
        # # print(reformed_datetime)
        # time_due_str = reformed_datetime[1]
        # time_due_str1 = time_due_str.split(':')
        # hour_due = (int(time_due_str1[0]) + 5) % 12
        # #because it's weird
        # if hour_due == 0:
        #     hours = 12
        # else:
        #     hours = hour_due
        # hour_due_str = str(hours)
        # print(hour_due_str + ':' + time_due_str1[1])
        # date_due = reformed_datetime[0]

        reformed_datetime.replace('T',' ')
        reformed_datetime.replace('z', '')
        print(reformed_datetime)

        # format = "%Y-%m-%d %H:%M:%S"
        # dt_object = datetime.strptime(reformed_datetime, format)
        # print(dt_object)
        
        # print(reformed_datetime)
        #2021-11-22T20:00:00Z
        # print(datetime.due.strftime('%A %d-%m-%Y, %H:%M:%S'))
        # reformed_date = reformed_datetime[0]
        #2021-11-22
        # reformed_time = reformed_datetime[1]
        #20:00:00Z

        # print(reformed_date)
        # print(reformed_time)

    context = {
        "hw_data" : hw_data,
        "session_form" : Sessionform()
    }
    return render(request, 'hw_session/index.html', context)


def create_session(request):
    return render(request, 'hw_session/running.html', context={})