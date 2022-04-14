from dataclasses import field, fields
from fileinput import FileInput
from re import template
from django import forms
from django.forms import ModelForm, TextInput, modelformset_factory
from togra.models import *
from tempus_dominus.widgets import TimePicker
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class formAssignment(ModelForm):
    class Meta:
        model = Soal
        fields = ("judul", 'tipe', 'timer')

        labels = {
            "judul": "Title",
            "tipe": "Assignment Type",
            "timer": "Duration"
        }
        widgets = {
            'judul': forms.TextInput({'class': 'form-control form-control-lg'}),
            'tipe': forms.Select({'class': 'form-select', 'onchange': 'myfunc()'}, choices=[('1', 'Essay'), ('2', 'Python')]),
            'timer': TimePicker(options={
                'defaultDate': '1970-01-01T00:00:00',
                'collapse': False,
            }, attrs={
                'append': 'far fa-clock',
                'size': 'small',
                'icon_toggle': True,
            }),
        }


class formEditAssignment(ModelForm):
    class Meta:
        model = Soal
        fields = ("judul", 'timer')

        labels = {
            "judul": "Title",
            "timer": "Duration"
        }
        widgets = {
            'judul': forms.TextInput({'class': 'form-control form-control-lg'}),
            'timer': TimePicker(options={
                'useCurrent': False,
                'collapse': False,
            }, attrs={
                'append': 'far fa-clock',
                'size': 'small',
                'icon_toggle': True,
            },
            ),
        }


FormQuestSet = modelformset_factory(
    Pertanyaan,
    fields=('instruksi', 'jawaban_benar', 'pyfile'),
    extra=1,
    labels={
        "instruksi": "Question",
        "jawaban_benar": "Answer",
        "pyfile": "Python File (.py)"
    },

    widgets={
        'instruksi': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        'jawaban_benar': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        'pyfile': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'})
    },
)

FormEditQuestEsSet = modelformset_factory(
    Pertanyaan,
    fields=('instruksi', 'jawaban_benar'),
    extra=0,
    labels={
        "instruksi": "Question",
        "jawaban_benar": "Answer",
    },

    widgets={
        'instruksi': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        'jawaban_benar': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
    },
)

FormEditQuestPySet = modelformset_factory(
    Pertanyaan,
    fields=('instruksi', 'pyfile'),
    extra=0,
    labels={
        "instruksi": "Question",
    },

    widgets={
        'instruksi': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        'pyfile': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'})
    },
)


class formPeserta(ModelForm):
    class Meta:
        model = Peserta
        fields = ("nama_peserta",)
        labels = {"nama_peserta": "Nama Peserta", }
        widgets = {'nama_peserta': forms.TextInput({'class': 'form-control'}),
                   }


FormJawabanEs = modelformset_factory(
    Jawaban,
    fields=('jawaban',),
    extra=1,
    labels={
        "jawaban": "Jawaban",
    },

    widgets={
        'jawaban': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
    },
)

FormJawabanPy = modelformset_factory(
    Jawaban,
    fields=('pyfile',),
    extra=1,
    labels={
        "pyfile": "Python File (.py)",
    },

    widgets={
        'pyfile': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
    },
)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user