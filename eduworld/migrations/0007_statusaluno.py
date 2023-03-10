# Generated by Django 4.1.1 on 2022-11-16 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0006_pdfassignments_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusAluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Submitted, Graded', 'Submitted, Graded'), ('Submitted', 'Submitted'), ('Not submitted yet', 'Not submitted yet')], default='Not submitted yet', max_length=26)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ALUNO', to=settings.AUTH_USER_MODEL)),
                ('atividadePDF', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PDF', to='eduworld.pdfassignments')),
            ],
        ),
    ]
