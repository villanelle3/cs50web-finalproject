from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
import datetime
from tinymce.models import HTMLField
from mptt.models import TreeForeignKey, MPTTModel


CHOICES = (
    ('primary','Primary [elementary] School'),
    ('midle', 'Midle School'),
    ('secondary','Secondary [high] School'),
    ('postsecondary','Postsecondary [tertiary] Education'),
)

SUB = (
    ('miss','Miss'),
    ('professor', 'Professor'),
    ('mrs','Mrs.'),
    ('mr','Mr.'),
    ('dr','Dr.'),
)

STATUS = (
    ('Submitted, Graded','Submitted, Graded'),
    ('Submitted','Submitted'),
    ('Missed', 'Missed'),
    ('Not submitted yet','Not submitted yet'),
)

class User(AbstractUser):
    pass

class Aluno(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_id")
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    school = models.CharField(max_length=300)
    level = models.CharField(max_length=300)
    completo = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} {self.last_name}."

class Teacher(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="usuario_id")
    call = models.CharField(max_length=300)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    completo = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} {self.last_name}."

class Classe(models.Model):
    id = models.IntegerField(primary_key=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Teacherr")
    name = models.CharField(max_length=300)
    section = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    room = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=200)
    data = models.DateTimeField(default=datetime.datetime.now)
    alunos = models.ManyToManyField(Aluno, related_name="alunoss", default=None, blank=True)
    alunos_count = models.BigIntegerField(default="0")
    def __str__(self):
        return f"{self.name}."

class PDFAssignments(models.Model):
    id = models.IntegerField(primary_key=True) # ID do assign
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="ClasseId") # Em qual classe o post esta
    pdf = models.FileField(null=True, blank=True, upload_to="pdfs/")

    titulo = models.CharField(max_length=500, blank=True, null=True)
    descrição = models.TextField(blank=True, null=True) # Post em si

    due_date = models.CharField(max_length=500, blank=True, null=True)
    due_hour = models.CharField(max_length=500, blank=True, null=True)
    points = models.IntegerField()

    def __str__(self):
        return f"{self.titulo}."

class StatusAluno(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ALUNO")
    atividadePDF = models.ForeignKey(PDFAssignments, on_delete=models.CASCADE, related_name="PDF")
    status = models.CharField(max_length=26, choices=STATUS, default='Not submitted yet')
    grade = models.IntegerField(blank=True, null=True)
    gradeLetter = models.CharField(max_length=3, blank=True, null=True)
    pdf = models.FileField(null=True, blank=True, upload_to="pdfs/")
    data_de_envio = models.CharField(max_length=500, blank=True, null=True)

class PrivateComments(models.Model):
    id = models.IntegerField(primary_key=True) # ID do post
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="aluninho")
    atividade = models.ForeignKey(PDFAssignments, on_delete=models.CASCADE, related_name="atvd")
    texto = models.TextField() # Post em si
    data = models.DateTimeField(default=datetime.datetime.now)
    has_reply = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.aluno} - > {self.texto}."

class ReplyPrivateComments(models.Model):
    id = models.IntegerField(primary_key=True) # ID do post
    atividade = models.ForeignKey(PDFAssignments, on_delete=models.CASCADE, related_name="atvdm")
    coment_inicial = models.ForeignKey(PrivateComments, on_delete=models.CASCADE, related_name="replytothatpost")
    texto = models.TextField() # Post em si
    data = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return f"{self.texto}."

class ForumPost(models.Model):
    id = models.IntegerField(primary_key=True) # ID do post
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DONO_DO_POST_FORUM") # Dono do post
    post_text = RichTextField(blank=True, null=True)
    data = models.DateTimeField(default=datetime.datetime.now)
    reply_count = models.BigIntegerField(default="0")
    views = models.BigIntegerField(default="0")
    category = models.CharField(max_length=300, blank=True, null=True)
    titulo = models.CharField(max_length=200)
    edited = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.titulo}."

class ReplyForumComments(models.Model):
    id = models.IntegerField(primary_key=True) # ID do post
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name="ForumPostreply")
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DONO_DO_RESOPSTA") # Dono do post
    texto = RichTextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="pessoasss", default=None, blank=True) ###########3
    data = models.DateTimeField(default=datetime.datetime.now)
    like_count = models.BigIntegerField(default="0")
    def __str__(self):
        return f"{self.texto}."


class ClassePosts(models.Model):
    id = models.IntegerField(primary_key=True) # ID do post
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="Classe_id") # Em qual classe o post esta
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DONO_DO_POST") # Dono do post
    #post_text = models.TextField() # Post em si
    post_text = RichTextField(blank=True, null=True)
    data = models.DateTimeField(default=datetime.datetime.now)
    reply_count = models.BigIntegerField(default="0")
    def __str__(self):
        return f"CLASSE: {self.classe} - > {self.post_text}."

class ReplyPosts(MPTTModel):
    id = models.IntegerField(primary_key=True) # ID da resposta
    post = models.ForeignKey(ClassePosts, on_delete=models.CASCADE, related_name="comments") # Em qual post foi o comentario
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DONO_DO_COMENTARIO") # Dono do comentario
    nome = models.CharField(max_length=500)
    data = models.DateTimeField(default=datetime.datetime.now)
    foto = models.CharField(max_length=500)
    text = models.TextField()
    reply_count = models.BigIntegerField(default="0")
    status = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    class MPTTMeta:
        order_insertion_by = ['data']
    def __str__(self):
        return f"{self.nome} - > {self.text}."

class Gadgets(models.Model):
    id = models.IntegerField(primary_key=True)
    imagem = models.ImageField(upload_to="images/")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    def __str__(self):
        return f"{self.titulo}."

class Complementos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MoreUser")
    bio = models.TextField(blank=True)

    collection = models.ManyToManyField(Gadgets) ###########
    collection_number = models.BigIntegerField(default="0") ###########

    classmates = models.ManyToManyField(Aluno, related_name="alunosss", default=None, blank=True) ###########3
    classmates_number = models.BigIntegerField(default="0") ##############2

    connections = models.ManyToManyField(User, related_name="pessoas", default=None, blank=True)
    connections_number = models.BigIntegerField(default="0")

    library_itens = models.CharField(max_length=200, blank=True)
    library_itens_number = models.BigIntegerField(default="0")

    saring_score = models.BigIntegerField(default="0")
    foto = models.ImageField(null=True, blank=True, upload_to="images/") ##############

    def __str__(self):
        return f"{self.usuario}."



