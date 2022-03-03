from cgitb import html
from cmath import e
from tkinter import LAST
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from togra.forms import *
from togra.models import *
from django.forms import modelformset_factory

def landing(request):
    return render(request, 'index.html')

def home(request):
    soals = Soal.objects.all()
    return render(request, 'table.html', {'soals' : soals,})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def NewAssignment(request):
    form = formAssignment()
    formset = FormQuestSet(queryset=Pertanyaan.objects.none())
    print("aaaaaaaaaaaaaaaaaaaa")
    konteks = {
        'form': form,
        'formset' : formset,
    }
    return render(request, 'form.html', konteks)

def AddAssign(request):
    form = formAssignment(request.POST)
    formset = FormQuestSet(request.POST)
    print("bbbbbbbbbbbbbbbb")
    if form.is_valid() and formset.is_valid():
        form.save()
        for f in formset:
            f.instance.soal_id = Soal.objects.latest('id')
            f.save()
            print("cccccccccccccccc")
    return redirect('/home/')

def EditAssign(request, soal_id):
    soal = Soal.objects.get(id=soal_id)
    if request.POST:
        form = formAssignment(request.POST)
        formset = FormEditQuestSet(request.POST)
        print("bbbbbbbbbbbbbbbb")
        if form.is_valid() and formset.is_valid():
            form.save()
            for f in formset:
                f.instance.soal_id = Soal.objects.latest('id')
                f.save()
                print("cccccccccccccccc")
        return redirect('/home/')
    else:
        form = formAssignment(instance=soal)
        formset = FormEditQuestSet(queryset=Pertanyaan.objects.filter(soal_id=soal_id))
        print("aaaaaaaaaaaaaaaaaaaa")
        konteks = {
            'form': form,
            'formset' : formset,
        }
        return render(request, 'form.html', konteks)

def assignment(request):
    return render(request, 'assignment.html')