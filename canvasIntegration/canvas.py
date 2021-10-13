from canvasapi import Canvas

def printAssignments(courses):
    for course in courses:
        print('---------------------------------------')
        print(course)
        assignments = course.get_assignments(bucket='upcoming')
        for assignment in assignments:
            print(assignment)

def main():
    API_URL = "https://byui.instructure.com"
    API_KEY = "10706~g5MeRiNe5b7qFLAyArcWEiszgpQNqOyBEyjJdRNSHgWOMvBJWYEfQOINCDzfqqxI"
    canvas = Canvas(API_URL, API_KEY)
    myUserID = 167103

    user = canvas.get_user(myUserID)
    print(user)

    courses = user.get_courses(bucket='favorites')

    printAssignments(courses)

main()