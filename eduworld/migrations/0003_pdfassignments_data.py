# Generated by Django 4.1.1 on 2022-11-16 20:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0002_pdfassignments_descrição_pdfassignments_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfassignments',
            name='data',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
