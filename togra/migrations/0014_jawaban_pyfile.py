# Generated by Django 3.2.8 on 2022-04-03 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('togra', '0013_auto_20220403_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='jawaban',
            name='pyfile',
            field=models.FileField(default='No Data', null=True, upload_to='python/'),
        ),
    ]
