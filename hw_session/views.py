from django.http import request
from django.views.decorators.csrf import csrf_protect 
from django.shortcuts import render, redirect
from .forms import Sessionform
from .canvas import Canvas_Cl

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
    hw_data = canvas_cl.get_days(hw_data)

    context = {
        "hw_data" : hw_data,
        "session_form" : Sessionform()
    }
    return render(request, 'hw_session/index.html', context)