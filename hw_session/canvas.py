from canvasapi import Canvas
import threading
import json
from datetime import datetime
from .models import Hw_Data

class Canvas_Cl():

    def __init__(self):
        pass
    
    def refreshHwData(self):
        tasks = []
        hourOfReload = 0
        curHour = (datetime.now().hour % 12)
        # print("curHour: ", curHour)
        allHwData = Hw_Data.objects.all()
        # print("allHWData", allHwData)

        for assignment in allHwData:
            # print("assignment: ", assignment)
            tasks.append(assignment)
            dateTimeOfReload = assignment.loaded_at
            hourOfReload = ((dateTimeOfReload.hour + 5) % 12)
            # print("hourOfReload: ", hourOfReload)
        
        if curHour == hourOfReload:
            print("\nNo need to reload\n")
            # print(tasks)
            return tasks
        else:
            print("\nReload Data\n")

            Hw_Data.objects.all().delete()
            newData = self.getHWData()

            return newData
                
    #------------------------------------------------------------------------------
    # Gets all of the assignments for a given course
    #------------------------------------------------------------------------------
    def getCourseAssignments(self, course, results, lock):
    
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
                "is_selected" : False,
                "is_completed" : assignment.has_submitted_submissions
            })
            #Loaded assignments bug IS COMPLETED may not be a perfect binary indicator of assignments 
        # Any time we modify shared results obj use lock for protection
        with lock:
            results[course.id]['courseName'] = course.name
            # We only want the assignments that haven't been submitted yet
            results[course.id]['assignments'] = list(filter(lambda a: a['is_completed'] == False, assignmentList))


    #------------------------------------------------------------------------------
    # Starts a thread for each course to get its assignments.
    # The assignments are put into the results object as the threads
    # rejoin the main thread. The results object is then returned.
    # A lock is used to protect the results obj from race conditions.
    #------------------------------------------------------------------------------
    def getAllAssignments(self, courses):
        courseThreads = []
        results = {}
        lock = threading.Lock()

        # Create a thread for each course
        for course in courses:
            thread = threading.Thread(target=self.getCourseAssignments, args=(course, results, lock))
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
    def getHWData(self):
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
        results = self.getAllAssignments(courses)
        tasks = []

        for course in results:
            for assignment in results[course]['assignments']:
                hw =Hw_Data( 
                    name=assignment['name'], 
                    due_date=assignment['due_date'], 
                    course=assignment['course'], 
                    is_selected=assignment['is_selected'],
                    is_completed=assignment['is_completed']
                    )
                print('hw:', hw)
                hw.save()
                tasks.append(hw)
        return tasks


        