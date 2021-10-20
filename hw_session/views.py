from django.http import request
from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'hw_session/index.html', context)