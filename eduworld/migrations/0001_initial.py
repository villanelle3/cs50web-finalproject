# Generated by Django 4.1.1 on 2022-11-16 20:40

import ckeditor.fields
import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('school', models.CharField(max_length=300)),
                ('level', models.CharField(max_length=300)),
                ('completo', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('section', models.CharField(blank=True, max_length=200)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('room', models.CharField(blank=True, max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('alunos_count', models.BigIntegerField(default='0')),
                ('alunos', models.ManyToManyField(blank=True, default=None, related_name='alunoss', to='eduworld.aluno')),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Teacherr', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassePosts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('post_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('reply_count', models.BigIntegerField(default='0')),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Classe_id', to='eduworld.classe')),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DONO_DO_POST', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gadgets',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('imagem', models.ImageField(upload_to='images/')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('call', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('completo', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReplyPosts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=500)),
                ('data', models.DateTimeField(default=datetime.datetime.now)),
                ('foto', models.CharField(max_length=500)),
                ('text', models.TextField()),
                ('reply_count', models.BigIntegerField(default='0')),
                ('status', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('dono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DONO_DO_COMENTARIO', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='eduworld.replyposts')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='eduworld.classeposts')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PDFAssignments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ClasseId', to='eduworld.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Complementos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('collection_number', models.BigIntegerField(default='0')),
                ('classmates_number', models.BigIntegerField(default='0')),
                ('connections_number', models.BigIntegerField(default='0')),
                ('library_itens', models.CharField(blank=True, max_length=200)),
                ('library_itens_number', models.BigIntegerField(default='0')),
                ('saring_score', models.BigIntegerField(default='0')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('classmates', models.ManyToManyField(blank=True, default=None, related_name='alunosss', to='eduworld.aluno')),
                ('collection', models.ManyToManyField(to='eduworld.gadgets')),
                ('connections', models.ManyToManyField(blank=True, default=None, related_name='pessoas', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MoreUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]