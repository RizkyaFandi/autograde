from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import CharField

class Soal(models.Model):
    judul = models.CharField(max_length=100)
    timer = models.TimeField(null=True)
    tipe = models.CharField(max_length=10,null=True)
    link_soal = models.URLField(max_length=200,null=True)
    attempts = models.IntegerField(null=True)
    user = models.TextField(null=True)

    def __str__(self):
        return self.judul

class Pertanyaan(models.Model):
    instruksi = models.TextField()
    jawaban_benar = models.TextField(null=True, default="Answer")
    pyfile = models.FileField(null=True, upload_to="python/", default="No Data")
    soal_id = models.ForeignKey(Soal, on_delete=models.CASCADE)

    def __str__(self):
        return self.instruksi

class Peserta(models.Model):
    nama_peserta = models.CharField(max_length=50)
    nilai = models.IntegerField(null=True)
    attemptdate = models.DateTimeField(auto_now_add=True, null=True)
    soal_id = models.ForeignKey(Soal, on_delete=CASCADE)

    def __str__(self):
        return self.nama_peserta

class Jawaban(models.Model):
    jawaban = models.TextField(null=True, default="")
    pembahasan = models.TextField(null=True, default="")
    pyfile = models.FileField(null=True, upload_to="python/", default="No Data")
    pertanyaan_id = models.ForeignKey(Pertanyaan, on_delete=CASCADE)
    peserta_id = models.ForeignKey(Peserta, on_delete=CASCADE)

    def __str__(self):
        return self.jawaban
