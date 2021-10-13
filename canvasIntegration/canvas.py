from canvasapi import Canvas
import json

def printAssignments(courses):
    for course in courses:
        print('---------------------------------------')
        print(course)
        assignments = course.get_assignments(bucket='upcoming')
        for assignment in assignments:
            print(assignment)

def main():
    tokenJSON = {}
    with open('accessToken.json') as file:
        tokenJSON = json.load(file)

    API_URL = "https://byui.instructure.com"
    API_KEY = tokenJSON["token"]
    canvas = Canvas(API_URL, API_KEY)
    myUserID = 167103

    user = canvas.get_user(myUserID)
    print(user)

    courses = user.get_courses(bucket='favorites')

    printAssignments(courses)

main()