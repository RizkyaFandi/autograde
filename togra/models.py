from django.db import models
from django.db.models.deletion import CASCADE

class Akun(models.Model):
    nama = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=12)

    def __str__(self):
        return self.username

class Soal(models.Model):
    judul = models.CharField(max_length=100)
    timer = models.TimeField(null=True)
    tipe = models.CharField(max_length=10,null=True)
    link_soal = models.URLField(max_length=200,null=True)
    attempts = models.IntegerField(null=True)
    akun_id = models.ForeignKey(Akun, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.judul

class Pertanyaan(models.Model):
    instruksi = models.TextField()
    jawaban_benar = models.TextField(null=True, default="")
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
