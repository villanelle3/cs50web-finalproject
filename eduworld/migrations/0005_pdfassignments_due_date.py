# Generated by Django 4.1.1 on 2022-11-16 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0004_remove_pdfassignments_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfassignments',
            name='due_date',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]