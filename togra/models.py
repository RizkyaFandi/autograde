from django.db import models
from django.db.models.deletion import CASCADE

class Akun(models.Model):
    username = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=12)

class Soal(models.Model):
    judul = models.CharField(max_length=100)
    timer = models.DurationField(null=True)
    tanggal = models.DateTimeField()
    link_soal = models.URLField(max_length=200,null=True)
    attempts = models.IntegerField(null=True)
    akun_id = models.ForeignKey(Akun, on_delete=models.CASCADE, null=True)

class Pertanyaan(models.Model):
    tipe = models.CharField(max_length=10)
    instruksi = models.TextField()
    jawaban_benar = models.TextField()
    soal_id = models.ForeignKey(Soal, on_delete=models.CASCADE)

class Peserta(models.Model):
    nama_peserta = models.CharField(max_length=50)
    nilai = models.IntegerField(null=True)
    soal_id = models.ForeignKey(Soal, on_delete=CASCADE)

class Jawaban(models.Model):
    jawaban = models.TextField(null=True)
    pembahasan = models.TextField()
    pertanyaan_id = models.ForeignKey(Pertanyaan, on_delete=CASCADE)
    peserta_id = models.ForeignKey(Peserta, on_delete=CASCADE)
