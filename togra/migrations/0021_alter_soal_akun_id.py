# Generated by Django 3.2.8 on 2022-04-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('togra', '0020_auto_20220410_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soal',
            name='akun_id',
            field=models.TextField(),
        ),
    ]
