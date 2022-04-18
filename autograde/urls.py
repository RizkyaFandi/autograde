from unicodedata import name
import django
from django.contrib import admin
from django.urls import path, include
from togra.views import *
from autograde.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', landing),
    path('home/', home, name='home'),
    path('newassignment/', NewAssignment),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/landing/'), name='logout'),
    path('register/', register),
    path('assignment/<int:soal_id>/', csrf_exempt(assignment), name='assignment'),
    path('addassign/', AddAssign),
    path('editassign/<int:soal_id>/', EditAssign, name='edit_assign'),
    path('addedit/<int:soal_id>/', AddEdit, name='edit'),
    path('attemption/<int:soal_id>/<int:peserta_id>/', grade, name='grade'),
    path('addanswer/answer<int:soal_id>', answer, name='addanswer'),
    path('lti/', include('lti_provider.urls')),
    path('sendgrade/<int:soal_id>/<int:peserta_id>/', csrf_exempt(grader), name='send'),
    path('detail/<int:soal_id>/', detailQuest, name='detail'),
    path('answer/<int:soal_id>/<int:peserta_id>/', detailAnswer, name='answer'),
    path('delete/<int:soal_id>/', deleteAssignment, name='delete'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
