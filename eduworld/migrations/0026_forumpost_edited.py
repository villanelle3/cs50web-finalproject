# Generated by Django 4.1.1 on 2022-12-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0025_replyforumcomments_dono'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
