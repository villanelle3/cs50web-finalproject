# Generated by Django 4.1.1 on 2022-11-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0015_alter_privatecomments_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusaluno',
            name='data_de_envio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]