# Generated by Django 4.1.1 on 2022-11-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eduworld', '0021_forumpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='titulo',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
