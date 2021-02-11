# Generated by Django 3.0.7 on 2021-01-30 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiAuto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiautocode',
            name='ApiInput',
            field=models.TextField(default='input'),
        ),
        migrations.AddField(
            model_name='apiautocode',
            name='ApiMethod',
            field=models.TextField(default='get'),
        ),
        migrations.AddField(
            model_name='apiautocode',
            name='ApiParam',
            field=models.TextField(default='para'),
        ),
        migrations.AddField(
            model_name='apiautocode',
            name='expectResult',
            field=models.TextField(default='{}'),
        ),
    ]
