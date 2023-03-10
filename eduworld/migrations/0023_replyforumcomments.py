# Generated by Django 4.1.1 on 2022-12-01 18:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0022_forumpost_titulo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyForumComments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('texto', models.TextField()),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('like_count', models.BigIntegerField(default='0')),
                ('likes', models.ManyToManyField(blank=True, default=None, related_name='pessoasss', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ForumPostreply', to='eduworld.forumpost')),
            ],
        ),
    ]
