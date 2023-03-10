# Generated by Django 4.1.1 on 2022-11-26 20:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0018_privatecomments_has_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyPrivateComments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('texto', models.TextField()),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('coment_inicial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replytothatpost', to='eduworld.privatecomments')),
            ],
        ),
    ]
