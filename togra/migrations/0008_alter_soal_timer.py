# Generated by Django 3.2.8 on 2022-04-02 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('togra', '0007_alter_soal_timer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soal',
            name='timer',
            field=models.DurationField(null=True),
        ),
    ]
