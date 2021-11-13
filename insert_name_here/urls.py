"""insert_name_here URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hw_session import views as hw_session_views
from mindfullness import views as mindfullness_views
from Dashboard import views as dashboard_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hw_session_views.home, name='home'),
    path('hw_session/home', hw_session_views.home, name="home"),
    path('mindfullness/', mindfullness_views.home, name='mindfullness_home'),
    path('runningSession/', hw_session_views.create_session, name="running_session"),
    path('dashboard/', dashboard_views.dash, name = "dashboard")


]
