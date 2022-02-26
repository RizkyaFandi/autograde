from cmath import e
from tkinter import LAST
from django.forms import formset_factory
from django.shortcuts import render
from togra.forms import formAssignment, formQuest
from togra.models import *
from django.forms import modelformset_factory

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
        print("bbbbbbbbbbbbbbbb")
        if form.is_valid():
            form.save()
            print("cccccccccccccccc")
            form = formAssignment()

            konteks = {
                'form': form,
            }
            return render(request, 'table.html', konteks)

        konteks = {
            'form': form,
        }

        return render(request, 'form.html', konteks)
    else:
        form = formAssignment()
        form1 = formQuest()
        print("aaaaaaaaaaaaaaaaaaaa")
        konteks = {
            'form': form,
            'form1' : form1,
        }

        return render(request, 'form.html', konteks)

def AddQuest(request):
    form1 = modelformset_factory(formQuest)
    formset = form1()
    print("bbbbbbbbbbbbbbbb")
    if formset.is_valid():
        form1.instance.soal_id = Soal.objects.latest('id')
        form1.save()
        print("cccccccccccccccc")
        form1 = formQuest()
    konteks = {
        'form1': form1,
    }
    return render(request, 'table.html', konteks)

def assignment(request):
    return render(request, 'assignment.html')