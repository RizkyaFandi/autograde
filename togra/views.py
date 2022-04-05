from asyncio.windows_events import NULL
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def landing(request):
    return render(request, 'index.html')

def home(request):
    soals = Soal.objects.all()
    for soal in soals:
        soal.timer = str(soal.timer)
        if soal.timer == "00:00:00":
            soal.timer = "None"
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
    formset = FormQuestSet(request.POST, request.FILES)
    print("bbbbbbbbbbbbbbbb")
    if form.is_valid() and formset.is_valid():
        form.save()
        for f in formset:
            f.instance.soal_id = Soal.objects.latest('id')
            if form.instance.tipe == "1" and f.instance.pyfile != "No Data":
                f.instance.pyfile = "No Data"
            if form.instance.tipe == "2" and f.instance.jawaban_benar != "":
                f.instance.jawaban_benar = ""
            f.save()
            print("cccccccccccccccc")
    return redirect('/home/')

def EditAssign(request, soal_id):
    soal = Soal.objects.get(id=soal_id)
    if request.POST:
        form = formEditAssignment(request.POST)
        formset = FormEditQuestEsSet(request.POST, request.FILES)
        print("bbbbbbbbbbbbbbbb")
        if form.is_valid() and formset.is_valid():
            form.save()
            for f in formset:
                f.instance.soal_id = Soal.objects.latest('id')
                if form.instance.tipe == "1" and f.instance.pyfile != "No Data":
                    f.instance.pyfile = "No Data"
                if form.instance.tipe == "2" and f.instance.jawaban_benar != "":
                    f.instance.jawaban_benar = ""
                f.save()
                print("cccccccccccccccc")
        return redirect('/home/')
    else:
        form = formEditAssignment(instance=soal)
        if soal.tipe == "1":
            formset = FormEditQuestEsSet(queryset=Pertanyaan.objects.filter(soal_id=soal_id))
        else:
            formset = FormEditQuestPySet(queryset=Pertanyaan.objects.filter(soal_id=soal_id))
        print("aaaaaaaaaaaaaaaaaaaa")
        konteks = {
            'form': form,
            'formset' : formset,
        }
        return render(request, 'edit.html', konteks)

def assignment(request, soal_id):
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)  
    form = formPeserta()
    soal = Soal.objects.get(id=soal_id)
    if soal.tipe == '1':
        formset = FormJawabanEs(queryset=Jawaban.objects.none())
    else:
        formset = FormJawabanPy(queryset=Jawaban.objects.none())
    pertanyaanList = []
    print(soal.timer)
    if soal.timer != "None":
        countdown = str(soal.timer).split(":")
        hours = int(countdown[0])*3600000
        minutes = int(countdown[1])*60000
        seconds = int(countdown[2])*1000
        timer = hours+minutes+seconds
    for pertanyaan in pertanyaans:
        pertanyaanList.append(pertanyaan.instruksi)
    json_format = json.dumps(pertanyaanList)
    konteks = {
        'pertanyaans': pertanyaans,
        'soal': soal,
        'form' : form,
        'formset' : formset,
        'pertanyaanList': json_format,
        'timer' : timer,
    }
    return render(request, 'assignment.html', konteks)

def answer(request, soal_id):
    count = -1
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)
    soal = Soal.objects.get(id=soal_id)
    form = formPeserta(request.POST)
    if soal.tipe == '1':
        formset = FormJawabanEs(request.POST)
    else:
        formset = FormJawabanPy(request.POST, request.FILES)
    if form.is_valid() and formset.is_valid():
        form.instance.soal_id = soal
        form.save()
        for f in formset:
            if count == -1:
                count = count + 1
                continue
            print(f.instance.jawaban)
            if f.instance.jawaban == "":
                f.instance.jawaban = "None"
            f.instance.pertanyaan_id = pertanyaans[count]
            f.instance.peserta_id = Peserta.objects.latest('id')
            f.save()
            print("cccccccccccccccc")
            count = count + 1
    return redirect('send' , soal_id)

def grade(request, soal_id):
    soal = Soal.objects.get(id=soal_id)
    sgrade = .75*100
    konteks = {
        'sgrade' : sgrade,
        'soal' : soal
    }
    return render(request, 'attemption.html', konteks)

@csrf_exempt
def grader(request, soal_id):
    sgrade = .75
    soal = Soal.objects.get(id=soal_id)
    konteks = {
        'sgrade' : sgrade,
        'soal' : soal
    }
    return render(request, 'testlti.html', konteks)

def detailQuest(request, soal_id):
    pesertas = Peserta.objects.filter(soal_id_id=soal_id)
    soal = Soal.objects.get(id=soal_id)
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)
    konteks = {
        'pesertas' : pesertas,
        'soal' : soal,
        'pertanyaans' : pertanyaans,
    }
    return render(request, 'detail.html', konteks)

def detailAnswer(request):
    return render(request, 'answer.html')

def deleteAssignment(request, soal_id):
    soal = Soal.objects.filter(id=soal_id)
    soal.delete()
    messages.success(request, "Assignment has been deleted successfully!" )
    return redirect('/home/')