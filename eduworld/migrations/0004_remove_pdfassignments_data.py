# Generated by Django 4.1.1 on 2022-11-16 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0003_pdfassignments_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdfassignments',
            name='data',
        ),
    ]
