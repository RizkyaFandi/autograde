from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from togra.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', landing),
    path('home/', home),
    path('newassignment/', NewAssignment),
    path('login/', login),
    path('register/', register),
    path('assignment/view<int:soal_id>', assignment, name='assignment'),
    path('addassign/', AddAssign),
    path('editassign/edit<int:soal_id>', EditAssign, name='edit_assign'),
    path('attemption/', grade, name='grade'),
    path('addanswer/answer<int:soal_id>', answer, name='addanswer'),
    path('lti/', include('lti_provider.urls')),
]
