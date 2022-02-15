from django.shortcuts import render
from togra.forms import formAssignment, formQuest
from togra.models import *

def landing(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'table.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def addAssignment(request):
    if request.POST:
        form = formAssignment(request.POST)
        form1 = formQuest(request.POST)
        if form.is_valid():
            form.save()
            form = formAssignment()
            for form1 in request:
                form1.save()
                form1 = formQuest()

            return render(request, 'table.html')
    else:
        form = formAssignment()
        form1 = formQuest()

        konteks = {
            'form': form,
            'form1' : form1,
        }

    return render(request, 'form.html', konteks)
    
def assignment(request):
    return render(request, 'assignment.html')