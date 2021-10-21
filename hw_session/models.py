from django.db import models
import json
from canvasapi import Canvas
import threading



# Create your models here.
class hw_data(models):
    name = models.CharField(max_length=30)
    due_date = models.DateTimeField()
    course = models.CharField(max_length=30)
    completed = models.BooleanField()

    def get_user_info(self):
        with open("./static/accessToken.json") as file:
            userData = json.load(file)
        API_URL = "https://byui.instruture.com"
        API_KEY = userData["token"]
        canvas = Canvas(API_URL, API_KEY)
        userID = userData['user_id']

        return canvas.get_user(userID)

    def get_all_assignments(self):
        courseThreads = []
        results = {}
        lock = threading.Lock()
        user = self.get_user_info()
        courses = user.get_courses(enrollment_state="active")

        for course in courses:
            thread = threading.Thread(target=self.get_assignments, args=(course, results, lock))
            courseThreads.append(thread)

        for thread in courseThreads:
            thread.start()

        for thread in courseThreads:
            thread.join()
        
        return results

    def get_assignments(self, course, results, lock):
        assignmentList = []
        results[course.id] = {
            "courseName": '',
            "assignments": []
        }
        assignments = course.get_assignments(bucket='upcoming')
        for assignment in assignments:
            assignmentList.append({
                "name" : assignment.name,
                "due_date" : assignment.due_at,
                "course" : course.name,
                "course_id" : course.id,
                "submitted" : assignment.has_submitted_submissions
            })
        
        with lock:
            results[course.id]['courseName'] = course.name
            results[course.id]['assignments'] = list(filter(lambda a: a['submitted'] == False, assignmentList))


class session_data(models):
    goal = models.CharField()
    time_limit = models.FloatField()
    selected_assignments = models.JSONField()
    start_time = models.DateTimeField()