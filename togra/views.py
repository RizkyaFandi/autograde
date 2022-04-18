from asyncio.windows_events import NULL
from cgitb import html
from unicodedata import name
from django.forms import formset_factory
from django.shortcuts import redirect, render
from autograde.settings import LOGIN_URL
from togra.forms import *
from togra.models import *
from django.forms import modelformset_factory
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def landing(request):
    return render(request, 'index.html')


@login_required(login_url=LOGIN_URL)
def home(request):
    soals = Soal.objects.filter(user=request.user.username)
    for soal in soals:
        soal.timer = str(soal.timer)
        if soal.timer == "00:00:00":
            soal.timer = "None"
    return render(request, 'table.html', {'soals': soals, })


def register(request):
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
            login(request, user)
            return redirect('home')
        else:
            messages.error = 'ERROR : Please check your input!'
            return redirect('/register/')
    else:
        form = NewUserForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url=LOGIN_URL)
def NewAssignment(request):
    form = formAssignment()
    formset = FormQuestSet(queryset=Pertanyaan.objects.none())
    print("aaaaaaaaaaaaaaaaaaaa")
    konteks = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'form.html', konteks)


@login_required(login_url=LOGIN_URL)
def AddAssign(request):
    form = formAssignment(request.POST)
    formset = FormQuestSet(request.POST, request.FILES)
    print(User.username)
    print("bbbbbbbbbbbbbbbb")
    if form.is_valid() and formset.is_valid():
        link = str(Soal.objects.latest('id').id + 1)
        form.instance.link_soal = 'http://127.0.0.1:8000/assignment/' + link + '/'
        form.instance.user = request.user.username
        form.save()
        for f in formset:
            f.instance.soal_id = Soal.objects.latest('id')
            if form.instance.tipe == "1":
                f.instance.pyfile = "No Data"
            else:
                f.instance.jawaban_benar = ""
            f.save()
            print("cccccccccccccccc")
    return redirect('/home/')


@login_required(login_url=LOGIN_URL)
def EditAssign(request, soal_id):
    soal = Soal.objects.get(id=soal_id)
    form = formEditAssignment(instance=soal)
    if soal.tipe == "1":
        formset = FormEditQuestEsSet(instance=soal)
    else:
        formset = FormEditQuestPySet(instance=soal)
    print("aaaaaaaaaaaaaaaaaaaa")
    konteks = {
        'form': form,
        'formset': formset,
        'soal': soal,
    }
    return render(request, 'edit.html', konteks)


@login_required(login_url=LOGIN_URL)
def AddEdit(request, soal_id):
    soal = Soal.objects.get(id=soal_id)
    form = formEditAssignment(request.POST, instance=soal)
    if soal.tipe == "1":
        formset = FormEditQuestEsSet(request.POST, instance=soal)
    else:
        formset = FormEditQuestPySet(
            request.POST, request.FILES, instance=soal)
    if form.is_valid() and formset.is_valid():
        print('asasas')
        form.save()
        formset.save()
        return redirect('/home/')


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
        'form': form,
        'formset': formset,
        'pertanyaanList': json_format,
        'timer': timer,
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
        peserta = Peserta.objects.latest('id')
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
        att = Soal.objects.get(id=soal_id)
        print(att.attempts)
        if att.attempts is None:
            att = 1
        else:
            att = att.attempts + 1
        Soal.objects.filter(id=soal_id).update(attempts=att)
    return redirect('send', soal_id, peserta.id)


def grade(request, soal_id, peserta_id):
    soal = Soal.objects.get(id=soal_id)
    peserta = Peserta.objects.get(id=peserta_id)
    sgrade = peserta.nilai
    konteks = {
        'sgrade': sgrade,
        'soal': soal
    }
    return render(request, 'attemption.html', konteks)


@csrf_exempt
def grader(request, soal_id, peserta_id):
    peserta = Peserta.objects.get(id=peserta_id)
    sgrade = .75
    grade = sgrade*100
    feedback = ''
    Peserta.objects.filter(id=peserta_id).update(nilai=grade)
    soal = Soal.objects.get(id=soal_id)
    konteks = {
        'sgrade': sgrade,
        'soal': soal,
        'peserta': peserta,
    }
    return render(request, 'testlti.html', konteks)


@login_required(login_url=LOGIN_URL)
def detailQuest(request, soal_id):
    pesertas = Peserta.objects.filter(soal_id_id=soal_id)
    soal = Soal.objects.get(id=soal_id)
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)
    timer = str(soal.timer)
    pyt = False
    if soal.tipe == '2':
        pyt = True
    konteks = {
        'pesertas': pesertas,
        'soal': soal,
        'pertanyaans': pertanyaans,
        'timer': timer,
        'python': pyt,
    }
    return render(request, 'detail.html', konteks)


@login_required(login_url=LOGIN_URL)
def detailAnswer(request, soal_id, peserta_id):
    peserta = Peserta.objects.get(id=peserta_id)
    pertanyaans = Pertanyaan.objects.filter(soal_id_id=soal_id)
    print(pertanyaans)
    for pertanyaan in pertanyaans:
        jawaban = Jawaban.objects.filter(
            pertanyaan_id_id=pertanyaan.id, peserta_id_id=peserta_id)

    for j in jawaban:
        if j.jawaban == "None":
            j.jawaban = NULL
    konteks = {
        'peserta': peserta,
        'jawaban': jawaban,
    }
    return render(request, 'answer.html', konteks)


@login_required(login_url=LOGIN_URL)
def deleteAssignment(request, soal_id):
    soal = Soal.objects.filter(id=soal_id)
    soal.delete()
    messages.success(request, "Assignment has been deleted successfully!")
    return redirect('/home/')
