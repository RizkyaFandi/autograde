from cgitb import html
from cmath import e
from tkinter import LAST
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from togra.forms import *
from togra.models import *
from django.forms import modelformset_factory
import json

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

def assignment(request, soal_id):
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)  
    form = formPeserta(request.POST)
    formset = FormJawaban(queryset=Jawaban.objects.none())
    soal = Soal.objects.get(id=soal_id)
    pertanyaanList = []
    for pertanyaan in pertanyaans:
        pertanyaanList.append(pertanyaan.instruksi)
    json_format = json.dumps(pertanyaanList)
    return render(request, 'assignment.html', {'pertanyaans': pertanyaans, 'soal': soal, 'form' : form, 'formset' : formset, 'pertanyaanList': json_format})

def answer(request, soal_id):
    count = -1
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)
    soal = Soal.objects.get(id=soal_id)
    form = formPeserta(request.POST)
    formset = FormJawaban(request.POST)
    if form.is_valid() and formset.is_valid():
        form.instance.soal_id = soal
        form.save()
        for f in formset:
            if count == -1:
                count = count + 1
                continue
            print(f.instance.jawaban)
            f.instance.pertanyaan_id = pertanyaans[count]
            f.instance.peserta_id = Peserta.objects.latest('id')
            f.save()
            print("cccccccccccccccc")
            count = count + 1
    return redirect('/attemption/')

def grade(request):
    return render(request, 'attemption.html')