from django.contrib import admin
from django.urls import path
from togra.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', landing),
    path('home/', home),
    path('newassignment/', addAssignment),
    path('login/', login),
    path('register/', register),
    path('assignment/', assignment),
    path('newquest/', AddQuest),
]
