from dataclasses import field, fields
from django import forms
from django.forms import ModelForm, modelformset_factory
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


FormQuestSet = modelformset_factory(
    Pertanyaan,
    fields= ('tipe', 'instruksi', 'jawaban_benar'),
    extra=1,
    labels = {
    "tipe": "Question Type",
    "instruksi": "Question", 
    "jawaban_benar": "Answer",
    },

    widgets = {
        'tipe' : forms.Select({'class' : 'form-select'}, choices=[('1','Essay'),('2','Python')]),
         'instruksi' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
        'jawaban_benar' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
    },
)

FormEditQuestSet = modelformset_factory(
    Pertanyaan,
    fields= ('tipe', 'instruksi', 'jawaban_benar'),
    extra=0,
    labels = {
    "tipe": "Question Type",
    "instruksi": "Question", 
    "jawaban_benar": "Answer",
    },

    widgets = {
        'tipe' : forms.Select({'class' : 'form-select'}, choices=[('1','Essay'),('2','Python')]),
         'instruksi' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
        'jawaban_benar' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
    },
)

class formPeserta(ModelForm):
    class Meta:
        model = Peserta
        fields = ("nama_peserta",)
        labels = {"nama_peserta": "Nama Peserta",}
        widgets = {'nama_peserta' : forms.TextInput({'class' : 'form-control'}),}

FormJawaban = modelformset_factory(
    Jawaban,
    fields= ('jawaban',),
    extra=1,
    labels = {
    "jawaban": "Jawaban",
    },

    widgets = {
        'jawaban' : forms.Textarea(attrs={'class' : 'form-control', 'rows': '3'}),
    },
)