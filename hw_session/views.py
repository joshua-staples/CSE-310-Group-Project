from django.http import request
from django.shortcuts import render
from canvasapi import Canvas
from .models import Hw_Data, Session_Data
import threading
import json
import random
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
        print("loaded it!")
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
        # print('current course id:', course)
        for assignment in results[course]['assignments']:
            # print('Current assignment:', assignment)
            hw = Hw_Data(
                name=assignment['name'], 
                due_date=assignment['due_date'], 
                course=assignment['course'], 
                submitted=assignment['submitted']
                )
            print('hw:', hw.name)
            hw.save()
            tasks.append(hw)
    return tasks

# Get random image to pass in as context.
def getImage():
    #import json file
    with open('./hw_session/static/images/photos.json') as file:
        imageDict = json.load(file)
        img = random.choice(list(imageDict))
        return imageDict[img]


# Create your views here.
def home(request):
    hw_data = getHWData()
    img_data = getImage()
    context = {
        "hw_data" : hw_data,
        "img_data" : img_data
    }
    return render(request, 'hw_session/hwSession.html', context)