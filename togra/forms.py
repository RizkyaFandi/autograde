from dataclasses import field
from django import forms
from django.forms import ModelForm
from togra.models import *
from tempus_dominus.widgets import DateTimePicker

class formAssignment(ModelForm):
    class Meta:
        model = Soal
        fields = ("judul", "tanggal")

        labels = {
        "judul": "Title",
        "tanggal": "Deadline",
    }
        widgets = {
            'judul' : forms.TextInput({'class' : 'form-control form-control-lg'}),
            'tanggal' : DateTimePicker(options={
                'useCurrent': True,
                'collapse': False,
            },attrs={
                'append': 'fa fa-calendar',
                'size': 'small',
                'icon_toggle': True,
            }),
        }

class formQuest(ModelForm):
    class Meta:
        model = Pertanyaan
        fields = ('tipe', 'instruksi', 'jawaban_benar')

        labels = {
        "tipe": "Question Type",
        "instruksi": "Question",
        "jawaban_benar": "Answer",
        }
        widgets = {
            'tipe' : forms.Select({'class' : 'form-select'}, choices=[('1','Essay'),('2','Python')]),
            'instruksi' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
            'jawaban_benar' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
        }