import random
import string
import json
import numpy as np
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import User, Aluno, Teacher, Classe, Complementos, ClassePosts, ReplyPosts, PDFAssignments
from .models import StatusAluno, PrivateComments, ReplyPrivateComments, ForumPost, ReplyForumComments
from django import forms
from django.forms import ModelForm
from django.views.generic import View
from datetime import date, datetime
from .widget import DatePickerInput

POSTDATA = "global"
POSTFOTO = "global"
POSTNOME = "global"
CLASSE = "global"

class imagem(ModelForm):
	class Meta:
		model = Complementos
		fields = ('foto',)
		labels = {
			'profile_picture': '',
		}

class NewPost(forms.ModelForm):
    class Meta:
        model = ClassePosts
        fields = ('post_text',)
        labels = {
			'post_text': '',
		}
        widgets = {
            'Post': forms.Textarea(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'Share something with your class...'}),
        }

class NewForumPost(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('post_text',)
        labels = {
			'post_text': 'What are the details of your problem?',
		}
        widgets = {
            'Post': forms.Textarea(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':'More details...'}),
        }

class NewForumPostReply(forms.ModelForm):
    class Meta:
        model = ReplyForumComments
        fields = ('texto',)
        labels = {
			'texto': '',
		}
        widgets = {
            'Post': forms.Textarea(attrs={'autocomplete':'off', 'class':'form-control', 'placeholder':''}),
        }

class JsonView(View):
    def get(self, *args, **kwargs):
        upper = kwargs.get("num_posts")
        lower = upper - 5
        posts = POSTDATA[lower:upper]
        foto = POSTFOTO[lower:upper]
        nome = POSTNOME[lower:upper]
        posts_size = len(POSTDATA)
        size = True if upper >= posts_size else False
        return JsonResponse({"data": posts, "foto": foto, "nome": nome, "max": size, "CLASSE":CLASSE}, safe=False)


class ExampleForm(forms.Form):
        Due_date = forms.DateField(widget=DatePickerInput(attrs={'class': "form-control"}), label='')


def get_random_string(length):
    letters = string.ascii_lowercase + string.digits + string.punctuation
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def is_complete(pk):
    aluno = Aluno.objects.filter(usuario=pk).values('completo')
    prof = Teacher.objects.filter(usuario=pk).values('completo')
    if aluno or prof:
        return True
    else:
        return False

def aluno_ou_prof(pk):
    aluno = Aluno.objects.filter(usuario=pk).values('completo')
    if aluno:
        return 'student'
    else:
        prof = Teacher.objects.filter(usuario=pk).values('completo')
        if prof:
            return 'prof'
        else:
            return False

def index(request):
    if request.user.is_authenticated and is_complete(request.user.id):
        type_of_user = aluno_ou_prof(request.user.id)
        no_classes = True

        if type_of_user == 'student':
            data = Aluno.objects.filter(usuario=request.user.id).values()
            classes = Classe.objects.filter(alunos=data[0]['id']).values()
            if classes:
                no_classes = False
        else:
            data = Teacher.objects.filter(usuario=request.user.id).values()
            classes = Classe.objects.filter(dono=request.user.id).values()
            if classes:
                no_classes = False

        comps = Complementos.objects.filter(usuario=request.user.id).values()
        return render(request, "eduworld/index.html", {"type_of_user":type_of_user, "data":data, "no_classes":no_classes,
                                                        "classes":classes, "loc":comps[0]['foto']})

    elif request.user.is_authenticated and not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def joinclass(request):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    if request.method == 'POST' and aluno_ou_prof(request.user.id) == 'student':
        code = request.POST["code"]

        try:
            p = Classe.objects.get(code = code)
        except Exception:
            no_classes = True
            data = Aluno.objects.filter(usuario=request.user.id).values()
            classes = Classe.objects.filter(alunos=data[0]['id']).values()
            if classes:
                no_classes = False
            comps = Complementos.objects.filter(usuario=request.user.id).values()
            return render(request, "eduworld/index.html", {
                "message": "Invalid class code!",
                "tipo": "danger",
                "type_of_user":'student',
                "data":data,
                "no_classes":no_classes,
                "classes":classes,
                "loc":comps[0]['foto'],
            })

    # Evitar entrar 2 vezes na mesma sala
    try:
        esta_classe = Classe.objects.filter(code=code).values()
        esta_classe_id = int(esta_classe[0]['id']) #id desta classe

###################################################################################################################
        contents = Classe.objects.all()
        classes_que_ela_esta = []
        for content in contents:
            if(content.alunos.filter(usuario=request.user.id).exists()):
                classes_que_ela_esta.append(content.id) #lista de ids das classes que a pessoa já está
 ###################################################################################################################


        if esta_classe_id in classes_que_ela_esta:
            no_classes = True
            data = Aluno.objects.filter(usuario=request.user.id).values()
            classes = Classe.objects.filter(alunos=data[0]['id']).values()
            if classes:
                no_classes = False
            comps = Complementos.objects.filter(usuario=request.user.id).values()
            return render(request, "eduworld/index.html", {
                "message": "You are in this class already!",
                "tipo": "danger",
                "type_of_user":'student',
                "data":data,
                "no_classes":no_classes,
                "classes":classes,
                "loc":comps[0]['foto'],
            })


    except Exception as e:
        print(e)

    data = Aluno.objects.filter(usuario=request.user.id).values()
    id = data[0]['id']
    p.alunos.add(id) # Adicionei o aluno na classe


    numero = Classe.objects.filter(code = code).values('alunos_count', 'id') #numero de alunos na classe
    id_classe = numero[0]['id'] #id da classe
    numero = int(numero[0]['alunos_count'])
    numero += 1

    p.alunos_count = numero  # change field
    p.save() # this will update only

    atividades = PDFAssignments.objects.filter(classe_id = id_classe).values('id')

    if atividades:
        for i in range (len(atividades)):
            StatusAluno.objects.create(aluno = request.user, atividadePDF_id = atividades[i]['id'], status = 'Not submitted yet').save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def createclass(request):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    if request.method == 'POST' and aluno_ou_prof(request.user.id) == 'prof':

        NOME = request.POST["NOME"].capitalize()
        SECTION = request.POST["SECTION"]
        SUBJECT = request.POST["SUBJECT"].capitalize()
        ROOM = request.POST["ROOM"]
        class_code = get_random_string(50)

        Classe.objects.create(dono = request.user, name = NOME, section = SECTION, subject = SUBJECT, room = ROOM, code = class_code).save()

        ids = Classe.objects.filter(dono = request.user, name = NOME, code = class_code).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        Classe.objects.filter(dono = request.user, name = NOME, code = class_code, id=lista_de_ids[1]).delete()

    return HttpResponseRedirect(reverse("index"))


@login_required
def profile(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    else:
        type_of_user = aluno_ou_prof(pk)
        if type_of_user == 'student':
            data = Aluno.objects.filter(usuario=pk).values()
            id_aluno = data[0]['id']

            contents = Classe.objects.all()
            classes_que_ela_esta = []
            for content in contents:
                if(content.alunos.filter(usuario=pk).exists()):
                    classes_que_ela_esta.append(content.id) #lista de ids das classes que a pessoa já está

            if classes_que_ela_esta:
                alunos_na_classe = []
                for classe in classes_que_ela_esta:
                    _classe_ = get_object_or_404(Classe, id=classe)
                    for x in _classe_.alunos.all():
                        alunos_na_classe.append(x.id)

                classmates = set(alunos_na_classe)

                p = Complementos.objects.get(usuario = pk)
                for id in classmates:
                    try:
                        p.classmates.add(id) # Adicionei o colega de classe
                    except Exception as e:
                        print(e)
                p.classmates_number = int(len(classmates)) - 1  # change field. excluindo ele proprio
                p.save() # this will update only

        elif type_of_user == 'prof':
            data = Teacher.objects.filter(usuario=pk).values()

            contents = Classe.objects.filter(dono=pk).values('id')
            if contents:
                classes_que_ela_esta = []
                for i in range(len(contents)):
                        classes_que_ela_esta.append(contents[i]['id']) #lista de ids das classes que a pessoa já está ensinando

                alunos_na_classe = []
                for classe in classes_que_ela_esta:
                    _classe_ = get_object_or_404(Classe, id=classe)
                    for x in _classe_.alunos.all():
                        alunos_na_classe.append(x.id)

                classmates = set(alunos_na_classe)
                p = Complementos.objects.get(usuario = pk)
                for id in classmates:
                    try:
                        p.classmates.add(id) # Adicionei o colega de classe
                    except Exception as e:
                        print(e)
                p.classmates_number = int(len(classmates))  # change field
                p.save() # this will update only

        else:
            NOT_FOUND = True
            return render(request, "eduworld/profile.html", {"NOT_FOUND":NOT_FOUND})

        DONO = False
        if pk == request.user.id:
            DONO = True
        complementos = Complementos.objects.filter(usuario=pk).values()

        if type_of_user == 'student':
            try:
                classmates.remove(id_aluno)
            except Exception as e:
                print(e)

        lista_de_ids_de_user = []
        lista_de_fotos_de_user = []
        lista_de_names = []

        try:
            for id_aluno in classmates:
                info = Aluno.objects.filter(id=id_aluno).values('usuario', 'name', 'last_name')
                id_user = info[0]['usuario']
                nome = info[0]['name']
                last_nome = info[0]['last_name']
                foto_user = Complementos.objects.filter(usuario=id_user).values('foto')[0]['foto']
                lista_de_ids_de_user.append(id_user)
                lista_de_fotos_de_user.append(foto_user)
                lista_de_names.append(f'{nome} {last_nome}')

                friend_info = zip(lista_de_fotos_de_user, lista_de_ids_de_user)
        except Exception as e:
            friend_info = False
            print(e)
        perfis = zip(lista_de_fotos_de_user, lista_de_ids_de_user, lista_de_names)

        if len(lista_de_ids_de_user) > 5:
            friend_info = zip(lista_de_fotos_de_user[0:5], lista_de_ids_de_user[0:5])

        arch_foto = []
        arch_titulo = []
        arch_desc = []

        _arch_ = get_object_or_404(Complementos, usuario=pk)
        for x in _arch_.collection.all():
            arch_foto.append(x.imagem)
            arch_titulo.append(x.titulo)
            arch_desc.append(x.descricao)

        arch = zip(arch_foto, arch_titulo, arch_desc)

        return render(request, "eduworld/profile.html", {"DONO":DONO, "data":data, "type_of_user":type_of_user, "pk": request.user.id,
                                                        "complementos":complementos, "loc":complementos[0]['foto'],
                                                        "friend_info":friend_info, "perfis":perfis, "arch":arch})


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eduworld/register.html", {
                "message": "Passwords must match.",
                "tipo": "danger"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "eduworld/register.html", {
                "message": "Email address already taken.",
                "tipo": "danger"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("complete", args=[user.id]))
    else:
        return render(request, "eduworld/register.html")

@login_required
def complete(request, pk):
    if request.method == "POST":

        titulo = None
        escola = None
        education = None

        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        try:
            titulo = request.POST["titulo"]
        except Exception as e:
            print(e)

        if titulo:
            print("É PROFESSOR")
            professor = Teacher.objects.create(usuario = request.user, name = firstname.capitalize(),
                                                last_name = lastname.capitalize(), call = titulo.capitalize(), completo = True)
            professor.save()

            complemento = Complementos.objects.create(usuario = request.user)
            complemento.save()

            # Remove the duplicate post

            ids = Teacher.objects.filter(name = firstname.capitalize(), usuario__username=request.user).values('id')
            lista_de_ids = []

            for i in range (len(ids)):
                lista_de_ids.append(ids[i]['id'])

            Teacher.objects.filter(name = firstname.capitalize(), usuario__username=request.user, id=lista_de_ids[1]).delete()

        else:
            escola = request.POST["escola"]
            education = request.POST["education"]
            print("É Aluno")
            aluno = Aluno.objects.create(usuario = request.user, name = firstname.capitalize(), last_name = lastname.capitalize(),
                                            school = escola.upper(), level = education.capitalize(), completo = True)
            aluno.save()

            complemento = Complementos.objects.create(usuario = request.user)
            complemento.save()

            # Remove the duplicate post

            ids = Aluno.objects.filter(name = firstname.capitalize(), usuario__username=request.user).values('id')
            lista_de_ids = []

            for i in range (len(ids)):
                lista_de_ids.append(ids[i]['id'])

            Aluno.objects.filter(name = firstname.capitalize(), usuario__username=request.user, id=lista_de_ids[1]).delete()

        return HttpResponseRedirect(reverse("index"))
    return render(request, "eduworld/complete.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "eduworld/login.html", {
                "message": "Invalid username and/or password.",
                "tipo": "danger"
            })
    else:
        return render(request, "eduworld/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def classroom(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))

    NOT_FOUND = False
    data = Classe.objects.filter(id = pk).values()
    if not data:
        NOT_FOUND = True
        return render(request, "eduworld/classe.html", {"NOT_FOUND":NOT_FOUND})

    dono_user_id = Classe.objects.filter(id = pk).values('dono')[0]['dono'] #user_id do dono

    infor = Teacher.objects.filter(usuario=dono_user_id).values('name', 'call', 'last_name')
    dono = f"{infor[0]['call']} {infor[0]['name']} {infor[0]['last_name']}"

    teacher_pic = Complementos.objects.filter(usuario=dono_user_id).values('foto')[0]['foto']

    DONO = False
    if dono_user_id == request.user.id:
        DONO = True

    posts = ClassePosts.objects.filter(classe = pk).values().order_by('-data').distinct()

    lista_de_nomes = []
    lista_de_fotos = []

    for i in range (len(posts)):
        ID = posts[i]['dono_id']
        type_of_user = aluno_ou_prof(ID)
        if type_of_user == 'student':
            nome = Aluno.objects.filter(usuario=ID).values('name', 'last_name')
            nome = f"{nome[0]['name']} {nome[0]['last_name']}"
        else:
            nome = Teacher.objects.filter(usuario=ID).values('name', 'last_name', 'call')
            nome = f"{nome[0]['call']} {nome[0]['name']} {nome[0]['last_name']}"
        foto = Complementos.objects.filter(usuario=ID).values('foto')
        lista_de_nomes.append(nome)
        lista_de_fotos.append(foto[0]['foto'])

    posts_info = zip(lista_de_fotos, lista_de_nomes, posts)
    mudar_variavel(list(posts), lista_de_nomes, lista_de_fotos, pk)

    if request.method == "POST":
        if request.POST.get("postar"):
            novo_post = request.POST["post_text"]
            pr = Classe.objects.get(id=pk)
            ClassePosts.objects.create(classe = pr, dono = request.user, post_text = novo_post).save()
            # Remove the duplicate post
            ids = ClassePosts.objects.filter(dono = request.user, post_text = novo_post).values('id')
            lista_de_ids = []
            for i in range (len(ids)):
                lista_de_ids.append(ids[i]['id'])
            ClassePosts.objects.filter(dono = request.user, post_text = novo_post, id=lista_de_ids[1]).delete()
            return HttpResponseRedirect(reverse("classroom", args=[pk]))

    _classe_ = get_object_or_404(Classe, id=pk)
    alunos_na_classe = []
    for x in _classe_.alunos.all():
        alunos_na_classe.append(x.id)
    # id de aluno dos alunos na classe

    lista_de_nomes_alunos = []
    lista_de_ids_alunos_users = []
    lista_de_fotos_alunos = []

    if len(alunos_na_classe) >= 1:
        for ident in alunos_na_classe:
            inf = Aluno.objects.filter(id=ident).values('name', 'last_name', 'usuario')
            nome = f"{inf[0]['name']} {inf[0]['last_name']}"
            lista_de_nomes_alunos.append(nome)
            lista_de_ids_alunos_users.append(inf[0]['usuario'])
            foto = Complementos.objects.filter(usuario=inf[0]['usuario']).values('foto')
            lista_de_fotos_alunos.append(foto[0]['foto'])
        students = zip(lista_de_nomes_alunos, lista_de_ids_alunos_users, lista_de_fotos_alunos, alunos_na_classe)
        students = sorted(students, key=lambda x: x[0])
    else:
        students = False
    nomes = False
    notas_de_cada_atividade = False
    assigments = PDFAssignments.objects.filter(classe=pk).values().order_by('id')
    today = date.today()
    d2 = today.strftime("%B %d, %Y") # Today
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'student':
        # Due dates
        due_dates = []
        titulos = []
        ids = []
        for x in range (len(assigments)):
            datetime_object = datetime.strptime(assigments[x]['due_date'], '%B %d, %Y')
            due_dates.append(datetime_object)
            titulos.append(assigments[x]['titulo'])
            ids.append(assigments[x]['id'])
        if len(due_dates) >= 1:
            currentDate = datetime.today()
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow = tomorrow.strftime('%A')
            today = currentDate.strftime('%A')
            datas_da_semana = []
            titulos_da_semana = []
            for x in range (len(due_dates)):
                assim = due_dates[x]
                dif = (assim - currentDate).total_seconds()
                if dif > 0 and dif <= 604800: # Atividades da semana
                    if assim.strftime('%A') == tomorrow:
                        datas_da_semana.append('Tomorrow') # Dia da atividade
                    elif assim.strftime('%A') == today:
                        datas_da_semana.append('Today') # Dia da atividade
                    else:
                        datas_da_semana.append(assim.strftime('%A')) # Dia da atividade
                    titulos_da_semana.append(titulos[x]) # titulo da atividade
                elif dif <= 0:
                    p = StatusAluno.objects.get(aluno=request.user.id, atividadePDF_id = ids[x])
                    if p.status == 'Not submitted yet':
                        p.status = 'Missed'  # change field
                        p.save() # this will update only
            if datas_da_semana:
                agenda = zip(titulos_da_semana, datas_da_semana)
            else:
                agenda = False
        else:
            agenda = False

        status = StatusAluno.objects.filter(aluno=request.user.id).values().order_by('atividadePDF_id')
        aluno_atv = zip(assigments, status)
    else:
        agenda = False # Prof
        aluno_atv = False
        idsatv = []
        listanotas = []
        notaspuras = []

        for x in range (len(assigments)):
            idsatv.append(assigments[x]['id'])

        for x in range (len(lista_de_ids_alunos_users)):
            for i in range(len(assigments)):
                nota = StatusAluno.objects.filter(aluno = lista_de_ids_alunos_users[x], atividadePDF_id = assigments[i]['id']).values()
                if i == 0:
                    listanotas.append(lista_de_nomes_alunos[x])
                listanotas.append(nota[0]["grade"])
                notaspuras.append(nota[0]["grade"])

        notas_de_cada_atividade = []
        splits = np.array_split(listanotas, int(len(lista_de_ids_alunos_users)))


        for array in splits:
            notas_de_cada_atividade.append(list(array))
        print(notas_de_cada_atividade)

        nomes = lista_de_nomes_alunos

    tam = int(len(assigments))
    return render(request, "eduworld/classe.html", {"data":data, "dono":dono, "DONO":DONO, "pk":pk, "posts":posts,
                                                    "posts_info":posts_info, "form":NewPost(), "assigments":assigments, "type_of_user":type_of_user,
                                                    "students":students, "teacher_name":dono, "teacher_id":dono_user_id, "teacher_pic":teacher_pic,
                                                    "aluno_atv":aluno_atv, "agenda":agenda, "nomes":nomes, "totalatv":tam,
                                                    "notas":notas_de_cada_atividade,})
def notaletter(nota):
    if int(nota) >= 90:
        return 'A+'
    elif int(nota) >= 85:
        return 'A'
    elif int(nota) >= 80:
        return'A-'
    elif int(nota) >= 77:
        return 'B+'
    elif int(nota) >= 73:
        return 'B'
    elif int(nota) >= 70:
        return 'B-'
    elif int(nota) >= 65:
        return 'C+'
    elif int(nota) >= 60:
        return 'C'
    elif int(nota) >= 55:
        return 'C-'
    elif int(nota) >= 50:
        return 'D'
    else:
        return 'F'


@login_required
def newassignment(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'student':
        return render(request, "eduworld/classe_post.html", {"proibido":True})

    if request.method == "POST":
        if request.POST.get("gradar"):
            nota = request.POST.get('nota', None)
            aluno = request.POST.get("gradar") # ID user
            p = StatusAluno.objects.get(aluno=aluno, atividadePDF_id = pk)
            p.grade = nota
            p.gradeLetter = notaletter(int(nota))
            if p.status == 'Submitted':
                p.status = 'Submitted, Graded'  # change field
            p.save() # this will update only

    assigment = PDFAssignments.objects.filter(id=pk).values()
    classe_id = assigment[0]["classe_id"]
    datetime_object = datetime.strptime(assigment[0]['due_date'], '%B %d, %Y')
    currentDate = datetime.today()
    dif = (datetime_object - currentDate).total_seconds()

    _classe_ = get_object_or_404(Classe, id = classe_id)
    alunos_na_classe = []
    for x in _classe_.alunos.all():
        alunos_na_classe.append(x.id) # IDs de alunos nas classes
    total = len(alunos_na_classe)
    lista_de_nomes_alunos = []
    lista_de_ids_alunos_users = []
    lista_de_status_alunos = []
    lista_de_pdfs_alunos = []
    datas_de_envio = []
    notas = []
    notasL = []
    turned_in = 0

    if len(alunos_na_classe) >= 1:
        for ident in alunos_na_classe:
            inf = Aluno.objects.filter(id=ident).values('name', 'last_name', 'usuario')
            nome = f"{inf[0]['name']} {inf[0]['last_name']}"
            lista_de_nomes_alunos.append(nome)
            lista_de_ids_alunos_users.append(inf[0]['usuario'])
        for id in lista_de_ids_alunos_users:
            if dif <= 0:
                p = StatusAluno.objects.get(aluno=id, atividadePDF_id = pk)
                if p.status == 'Not submitted yet':
                    p.status = 'Missed'  # change field
                    p.save() # this will update only
            stat = StatusAluno.objects.filter(aluno=id, atividadePDF_id = pk).values()
            lista_de_status_alunos.append(stat[0]['status'])
            if stat[0]['status'] == 'Submitted' or stat[0]['status'] == 'Submitted, Graded':
                turned_in += 1
            lista_de_pdfs_alunos.append(stat[0]['pdf'])
            datas_de_envio.append(stat[0]['data_de_envio'])
            notas.append(stat[0]['grade'])
            notasL.append(stat[0]['gradeLetter'])

        students = zip(lista_de_nomes_alunos, lista_de_ids_alunos_users, lista_de_status_alunos, lista_de_pdfs_alunos, datas_de_envio, notas, notasL)
        students = sorted(students, key=lambda x: x[0])
    else:
        students = False

    comments = PrivateComments.objects.filter(atividade_id = pk).values().order_by('-data')
    coment_info = False
    replies = False
    if comments:
        fotos = []
        nomes = []
        for i in range(len(comments)):
            nome = Aluno.objects.filter(usuario=comments[i]['aluno_id']).values('name', 'last_name')
            nome = f"{nome[0]['name']} {nome[0]['last_name']}"
            nomes.append(nome)
            foto = Complementos.objects.filter(usuario=comments[i]['aluno_id']).values('foto')
            fotos.append(foto[0]['foto'])
        coment_info = zip(comments, nomes, fotos)
        replies = ReplyPrivateComments.objects.filter(atividade_id = pk).values().order_by('-data')
        print(replies)
    return render(request, "eduworld/newassignment.html", {"assigment":assigment, "pk":pk, "students":students, "total":total, "turned_in":turned_in, "coment_info":coment_info,
                                                            "totalcoments":len(comments), "replies":replies})


@login_required
def assignment(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    # pk = atividade id
    r = False

    if request.method == "POST":
        if request.POST.get("salvarpdf"):
            form = request.FILES["updatpdf"]
            p = StatusAluno.objects.get(aluno=request.user.id, atividadePDF_id = pk)
            p.pdf = form
            p.status = "Submitted"
            today = date.today()
            d2 = today.strftime("%B %d, %Y") # Today
            p.data_de_envio = d2
            p.save()
            r = True
        elif request.POST.get("deletar"):
            postid = request.POST.get("deletar")
            post_a_ser_removido = get_object_or_404(PrivateComments, aluno=request.user.id, atividade_id = pk, id = postid)
            post_a_ser_removido.delete()

    assigment = PDFAssignments.objects.filter(id=pk).values()
    status = StatusAluno.objects.filter(aluno=request.user.id, atividadePDF_id = pk).values()
    comments = PrivateComments.objects.filter(aluno=request.user.id, atividade_id = pk).values().order_by('-data')


    nome = Aluno.objects.filter(usuario=request.user.id).values('name', 'last_name')
    nome = f"{nome[0]['name']} {nome[0]['last_name']}"
    foto = Complementos.objects.filter(usuario=request.user.id).values('foto')

    replies = ReplyPrivateComments.objects.filter(atividade_id = pk).values()

    if not status or not assigment:
        return HttpResponseRedirect(reverse("index"))
    if r:
        return render(request, "eduworld/assignment.html", {"assigment":assigment, "status":status,
                                                            "message": "Document successfully attached.",
                                                            "tipo": "success", "comments":comments, "nome":nome, "foto":foto[0]['foto'],
                                                            "pk":pk, "replies":replies})
    return render(request, "eduworld/assignment.html", {"assigment":assigment, "status":status, "comments":comments, "nome":nome, "foto":foto[0]['foto'],
                                                        "pk":pk, "replies":replies})

@login_required
def forum_index(request):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    if request.method == "POST":
        titulo = request.POST.get('titulo', None)
        category = request.POST.get('category', None)
        novo_post = request.POST["post_text"]
        ForumPost.objects.create(dono = request.user, category = category, post_text = novo_post, titulo = titulo).save()
        ids = ForumPost.objects.filter(dono = request.user, category = category, post_text = novo_post, titulo = titulo).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        ForumPost.objects.filter(dono = request.user, category = category, post_text = novo_post, titulo = titulo, id=lista_de_ids[1]).delete()
        return HttpResponseRedirect(reverse("forumquestion", args=[lista_de_ids[0]]))

    data = ForumPost.objects.all().values('dono_id__username', 'dono_id', 'titulo', 'data', 'category', 'reply_count', 'views', 'id').order_by('-data')

    p = Paginator(data, 6)
    page = request.GET.get('page')
    todas = p.get_page(page)
    nums = " " * todas.paginator.num_pages

    return render(request, "eduworld/forum_index.html", {"data":data, "form":NewForumPost(), 'todas': todas, 'nums': nums})


@login_required
def forum_question(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    data = ForumPost.objects.filter(id=pk).values()
    autor = ForumPost.objects.filter(id=pk).values('dono_id__username')
    autor = autor[0]['dono_id__username']
    if request.user.username == autor:
        dono = True
    else:
        dono = False
    replies = ReplyForumComments.objects.filter(post_id=pk).values('dono__username', 'data', 'texto', 'id', 'like_count').order_by('-like_count')
    contents = ReplyForumComments.objects.all()
    already_liked = []
    for content in contents:
       if(content.likes.filter(id = request.user.id).exists()):
        already_liked.append(content.id)
    print(already_liked)
    if request.method == 'POST' and dono:
        ForumPost.objects.filter(id = pk).delete()
        return HttpResponseRedirect(reverse("forum"))
    return render(request, "eduworld/question.html", {"pk":pk, "data":data, "autor":autor, "dono":dono, "replies":replies, "form":NewForumPostReply(),
                                                        "already_liked":already_liked})


@login_required
def search(request):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    if request.method == "POST":
        busca = request.POST.get('busca', None)
        ALUNOS_INFO = False
        PROFS_INFO = False
        GROUPS_INFO = False
        if busca:
            titulos = ForumPost.objects.filter(titulo__contains=busca).values()

            alunos_nomes = Aluno.objects.filter(name__contains=busca).values()
            alunos_last_name = Aluno.objects.filter(last_name__contains=busca).values()

            profs_nomes = Teacher.objects.filter(name__contains=busca).values()
            profs_last_name = Teacher.objects.filter(last_name__contains=busca).values()

            if titulos:
                titulos_valores = []
                titulos_valoresids = []
                for i in range(len(titulos)):
                    titulos_valores.append(titulos[i]['titulo'])
                    titulos_valoresids.append(titulos[i]['id'])
                GROUPS_INFO = zip(titulos_valores, titulos_valoresids)

            if alunos_nomes or alunos_last_name:
                alunos_names = []
                alunos_ids = []
                alunos_fotos = []
                for i in range(len(alunos_nomes)):
                    nome = f"{alunos_nomes[i]['name']} {alunos_nomes[i]['last_name']}"
                    alunos_names.append(nome)
                    alunos_ids.append(alunos_nomes[i]['usuario_id'])
                    foto = Complementos.objects.filter(usuario=alunos_nomes[i]['usuario_id']).values('foto')
                    alunos_fotos.append(foto[0]['foto'])
                for j in range(len(alunos_last_name)):
                    nome = f"{alunos_last_name[j]['name']} {alunos_last_name[j]['last_name']}"
                    alunos_names.append(nome)
                    alunos_ids.append(alunos_last_name[j]['usuario_id'])
                    foto = Complementos.objects.filter(usuario=alunos_last_name[j]['usuario_id']).values('foto')
                    alunos_fotos.append(foto[0]['foto'])
                ALUNOS_INFO = zip(alunos_names, alunos_ids, alunos_fotos)

            if profs_nomes or profs_last_name:
                profs_names = []
                profs_ids = []
                profs_fotos = []
                for i in range(len(profs_nomes)):
                    nome = f"{profs_nomes[i]['call']} {profs_nomes[i]['name']} {profs_nomes[i]['last_name']}"
                    profs_names.append(nome)
                    profs_ids.append(profs_nomes[i]['usuario_id'])
                    foto = Complementos.objects.filter(usuario=profs_nomes[i]['usuario_id']).values('foto')
                    profs_fotos.append(foto[0]['foto'])
                for j in range(len(profs_last_name)):
                    nome = f"{alunos_last_name[j]['call']} {alunos_last_name[j]['name']} {alunos_last_name[j]['last_name']}"
                    profs_names.append(nome)
                    profs_ids.append(alunos_last_name[j]['usuario_id'])
                    foto = Complementos.objects.filter(usuario=alunos_last_name[j]['usuario_id']).values('foto')
                    profs_fotos.append(foto[0]['foto'])
                PROFS_INFO = zip(profs_names, profs_ids, profs_fotos)

    return render(request, "eduworld/search.html", {"busca":busca, "PROFS_INFO":PROFS_INFO, "ALUNOS_INFO":ALUNOS_INFO, "GROUPS_INFO":GROUPS_INFO})


@csrf_exempt
def edit_data(request):
    if request.method == "POST":
        texto = request.POST.get('novocomentario', None)
        id = request.POST.get('postid', None)
        p = PrivateComments.objects.get(aluno=request.user.id, id = id)
        p.texto = texto
        p.save()
        print('veio aqui')
        return JsonResponse({'status': 'saved'}, safe=False)
    else:
        print('veio aqui no else')
        texto = request.POST.get('novocomentario', None)
        print(texto)
        return JsonResponse({'status': 'not saved'}, safe=False)

@csrf_exempt
def edittitulo(request):
    if request.method == "POST":
        texto = request.POST.get('novotitulo', None)
        id = request.POST.get('postid', None)
        p = ForumPost.objects.get(id = id)
        p.titulo = texto
        p.edited = True
        p.save()
        print('veio aqui')
        return JsonResponse({'status': 'saved'}, safe=False)
    else:
        print('veio aqui no else')
        return JsonResponse({'status': 'not saved'}, safe=False)

@csrf_exempt
def forum_filter(request):
    category = request.POST.get('category')
    if category:
        t = ForumPost.objects.filter(category__contains=category).values('dono_id__username', 'dono_id', 'titulo', 'data', 'category', 'reply_count', 'views', 'id').order_by('-data')
        return JsonResponse({'status': 'saved', 'dt':list(t)}, safe=False)
    else:
        return JsonResponse({'status': 'error'}, safe=False)


@csrf_exempt
def deletereply(request):
    if request.method == "POST":
        replyid = request.POST.get('replyid', None)
        print(replyid)
        ReplyPrivateComments.objects.filter(id = replyid).delete()
        return JsonResponse({'status': 'saved', 'replyid':replyid}, safe=False)
    else:
        print('veio aqui no else')
        texto = request.POST.get('novocomentario', None)
        print(texto)
        return JsonResponse({'status': 'not saved'}, safe=False)


@csrf_exempt
def deletepost(request, pk, classid):
    if request.method == "POST":
        print('veio aki')
        print(pk)
        ClassePosts.objects.filter(id = pk).delete()
        return HttpResponseRedirect(reverse("classroom", args=[classid]))
    else:
        print('veio aqui no else')
        return HttpResponseRedirect(request.path_info)


@csrf_exempt
def reply_coment(request):
    if request.method == "POST":
        texto = request.POST.get('novoreply', None) #reply body
        id = request.POST.get('postid', None) # coment_inicial_id
        pk = request.POST.get('pk', None) # atividade_id

        ReplyPrivateComments.objects.create(atividade_id = pk, texto = texto, coment_inicial_id = id).save()

        ids = ReplyPrivateComments.objects.filter(atividade_id = pk, texto = texto, coment_inicial_id = id).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        ReplyPrivateComments.objects.filter(atividade_id = pk, texto = texto, coment_inicial_id = id, id=lista_de_ids[1]).delete()

        p = PrivateComments.objects.get(id = id)
        p.has_reply = True
        p.save()
        print('veio aqui')

        myDate = datetime.now()
        ampm = myDate.strftime("%p")
        formatedDate = myDate.strftime("%b. %d, %Y, %-I:%S")
        datinha = f"{formatedDate} {ampm.lower()[0]}.{ampm.lower()[1]}"
        return JsonResponse({'status': 'saved', 'date':datinha, "id":id, "reply":texto, "replyid":lista_de_ids[0]}, safe=False)
    else:
        print('veio aqui no else')
        return JsonResponse({'status': 'not saved'}, safe=False)


@csrf_exempt
def add_data(request):
    if request.method == "POST":
        texto = request.POST.get('comentario', None)
        pk = request.POST.get('pk', None)
        PrivateComments.objects.create(aluno=request.user, atividade_id = pk, texto = texto).save()
        ids = PrivateComments.objects.filter(aluno=request.user.id, atividade_id = pk, texto = texto).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        PrivateComments.objects.filter(aluno=request.user.id, atividade_id = pk, texto = texto, id=lista_de_ids[1]).delete()

        comments = PrivateComments.objects.filter(aluno=request.user.id, atividade_id = pk, id=lista_de_ids[0]).values().order_by('-data')
        nome = Aluno.objects.filter(usuario=request.user.id).values('name', 'last_name')
        nome = f"{nome[0]['name']} {nome[0]['last_name']}"
        foto = Complementos.objects.filter(usuario=request.user.id).values('foto')

        myDate = datetime.now()
        ampm = myDate.strftime("%p")
        formatedDate = myDate.strftime("%b. %d, %Y, %-I:%S")

        datinha = f"{formatedDate} {ampm.lower()[0]}.{ampm.lower()[1]}"

        comendata = list(comments)
        return JsonResponse({'status': 'saved', 'comendata':comendata, 'nome':nome, 'foto':foto[0]['foto'], 'day':datinha}, safe=False)
    else:
        return JsonResponse({'status': 'not saved'}, safe=False)


@csrf_exempt
def add_like(request): #voltar
    if request.method == "POST":
        postid = request.POST.get('postid', None)
        post = get_object_or_404(ReplyForumComments, id=postid)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            post.save()
        return JsonResponse({'status': 'saved',}, safe=False)
    else:
        return JsonResponse({'status': 'not saved'}, safe=False)


@csrf_exempt
def editar_data(request):
    if request.method == "POST":
        pk = request.POST.get('pk', None)
        titulo = request.POST.get('titulo', None)
        desc = request.POST.get('desc', None)
        p = PDFAssignments.objects.get(id = pk)
        p.titulo = titulo
        p.descrição = desc
        p.save()
        return JsonResponse({'status': 'saved'}, safe=False)
    else:
        print('veio aqui no else')
        texto = request.POST.get('novocomentario', None)
        print(texto)
        return JsonResponse({'status': 'not saved'}, safe=False)


@login_required
def newformreply(request, pk):
    if request.method == "POST":
        texto = request.POST["texto"]
        if texto:
            ReplyForumComments.objects.create(post_id = pk, dono = request.user, texto = texto).save()
            ids = ReplyForumComments.objects.filter(post_id = pk, dono = request.user, texto = texto).values('id')
            lista_de_ids = []
            for i in range (len(ids)):
                lista_de_ids.append(ids[i]['id'])
            ReplyForumComments.objects.filter(post_id = pk, dono = request.user, texto = texto, id=lista_de_ids[1]).delete()

            p = ForumPost.objects.get(id=pk)
            p.reply_count += 1  # change field]
            p.save() # this will update only
    return HttpResponseRedirect(reverse("forumquestion", args=[pk])) #estou


def aluno_delete(request, classid, alunoid):
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'student' or not is_complete(request.user.id):
        return render(request, "eduworld/classe_post.html", {"proibido":True})
    dono_user_id = Classe.objects.filter(id = classid).values('dono')[0]['dono'] #user_id do dono
    if dono_user_id != request.user.id:
        return render(request, "eduworld/classe_post.html", {"proibido":True})

    if request.method == "POST":
        aluno_a_ser_removido = get_object_or_404(Aluno, id=alunoid)
        classe_d_aluno_a_ser_removido = get_object_or_404(Classe, id=classid)

        classe_d_aluno_a_ser_removido.alunos.remove(aluno_a_ser_removido)
        return HttpResponseRedirect(reverse("classroom", args=[classid]))


def cancel(request, pk):
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'student' or not is_complete(request.user.id):
        return render(request, "eduworld/classe_post.html", {"proibido":True})

    classe_id = PDFAssignments.objects.filter(id = pk).values('classe_id')[0]['classe_id'] #id da classe
    dono_user_id = Classe.objects.filter(id = classe_id).values('dono')[0]['dono'] #user_id do dono
    if dono_user_id != request.user.id:
        return render(request, "eduworld/classe_post.html", {"proibido":True})

    if request.method == "POST":
        assing_a_ser_removido = get_object_or_404(PDFAssignments, id=pk)
        assing_a_ser_removido.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def mes(n):
    if n == 1:
     return 'January'
    elif n == 2:
     return 'February'
    elif n == 3:
     return 'March'
    elif n == 4:
     return 'April'
    elif n == 5:
     return 'May'
    elif n == 6:
     return 'June'
    elif n == 7:
     return 'July'
    elif n == 8:
     return 'August'
    elif n == 9:
     return 'September'
    elif n == 10:
     return 'October'
    elif n == 11:
     return 'November'
    else:
     return 'December'


@login_required
def create_homework(request, pk):
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'student' or not is_complete(request.user.id):
        return render(request, "eduworld/classe_post.html", {"proibido":True})
    message = False
    tipo = False
    if request.method == "POST":
        print('veio aqui2')
        form = request.FILES["updatpdf"]
        titulo = request.POST["newtitle"]
        desc = request.POST["newdescription"]
        data = request.POST["Due_date"]

        x = data.split("-")
        ano = x[0]
        month = x[1]
        month = mes(int(month))
        day = x[2]

        data = f'{month} {day}, {ano}'

        print(data)
        message = "Assignment successfully created."
        tipo = "success"

        PDFAssignments.objects.create(classe_id = pk, pdf = form, titulo = titulo, descrição = desc, due_date = data, points = 100).save()
        ids = PDFAssignments.objects.filter(classe_id = pk, titulo = titulo, descrição = desc, due_date = data, points = 100).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        PDFAssignments.objects.filter(classe_id = pk, id=lista_de_ids[1]).delete()

        _classe_ = get_object_or_404(Classe, id=pk)
        alunos_na_classe = []
        for x in _classe_.alunos.all():
            alunos_na_classe.append(x.id)
        # id de aluno dos alunos na classe

        lista_de_ids_alunos_users = []

        if len(alunos_na_classe) >= 1:
            for ident in alunos_na_classe:
                inf = Aluno.objects.filter(id=ident).values('usuario')
                lista_de_ids_alunos_users.append(inf[0]['usuario'])

        for id in lista_de_ids_alunos_users:
            StatusAluno.objects.create(aluno_id = id, atividadePDF_id = lista_de_ids[0]).save()

    return render(request, "eduworld/homework.html", {"form":ExampleForm(), "message":message, "tipo":tipo})


def mudar_variavel(data, nome, foto, pk):
    global POSTDATA, POSTFOTO, POSTNOME, CLASSE
    POSTDATA = data
    POSTFOTO = foto
    POSTNOME = nome
    CLASSE = pk


@login_required
def classe_post(request, classid, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))

    # Informações da classe:
    classe = Classe.objects.filter(id = classid).values()

    if not classe:
        return render(request, "eduworld/classe.html", {"NOT_FOUND":True})
    type_of_user = aluno_ou_prof(request.user.id)
    if type_of_user == 'prof':
        dono = classe[0]['dono_id']
        if dono != request.user.id:
            return render(request, "eduworld/classe_post.html", {"proibido":True})
    else:
        aluno_id = Aluno.objects.filter(usuario__username=request.user).values()
        aluno_id = aluno_id[0]['id']
        _classe_ = get_object_or_404(Classe, id=classid)
        alunos_na_classe = []
        for x in _classe_.alunos.all():
            alunos_na_classe.append(x.id)
        if aluno_id not in alunos_na_classe:
            return render(request, "eduworld/classe_post.html", {"proibido":True})

    # Informações do post:
    post = ClassePosts.objects.filter(id = pk).values()
    if post[0]['dono_id'] == request.user.id:
        dono = True
    else:
        dono = False
    if not post:
        return render(request, "eduworld/classe_post.html", {"proibido":False, "not_found":True})

    dono_do_post_id = post[0]['dono_id']
    dono_tipo = aluno_ou_prof(dono_do_post_id)
    if dono_tipo == 'prof':
        infor = Teacher.objects.filter(usuario=dono_do_post_id ).values('name', 'call', 'last_name')
        nome = f"{infor[0]['call']} {infor[0]['name']} {infor[0]['last_name']}"
    else:
        infor = Aluno.objects.filter(usuario=dono_do_post_id ).values('name', 'last_name')
        nome = f"{infor[0]['name']} {infor[0]['last_name']}"
    foto = Complementos.objects.filter(usuario=dono_do_post_id).values('foto')

    # Informações sobre replies
    replies = ReplyPosts.objects.filter(post=pk).values().order_by('-data').distinct()

    return render(request, "eduworld/classe_post.html", {"proibido":False, "not_found":False, "classid":classid, "post_info":post, "nome":nome,
                                                        "foto":foto[0]['foto'], "replies":replies, "pk":pk, "dono":dono})

@login_required
@csrf_exempt
def addcomment(request):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))
    if request.method == "POST":
        comment = request.POST["comentario"]
        botao = request.POST["botao"]
        botao = request.POST.get("botao")

        x = botao.split(", ")
        type_of_user = aluno_ou_prof(request.user.id)
        if type_of_user == 'prof':
            infor = Teacher.objects.filter(usuario=request.user.id).values('name', 'call', 'last_name')
            nome = f"{infor[0]['call']} {infor[0]['name']} {infor[0]['last_name']}"
        else:
            infor = Aluno.objects.filter(usuario=request.user.id).values('name', 'last_name')
            nome = f"{infor[0]['name']} {infor[0]['last_name']}"
        foto = Complementos.objects.filter(usuario=request.user.id).values('foto')


        _post_ = get_object_or_404(ClassePosts, id=x[1])

        ReplyPosts.objects.create(post = _post_, dono = request.user, nome = nome, foto = foto, text = comment).save()
        ids = ReplyPosts.objects.filter(dono = request.user, post = _post_, text = comment).values('id')
        lista_de_ids = []
        for i in range (len(ids)):
            lista_de_ids.append(ids[i]['id'])
        ReplyPosts.objects.filter(dono = request.user, post = _post_, text = comment, id=lista_de_ids[1]).delete()

        p = ClassePosts.objects.get(id=x[1])
        p.reply_count += 1  # change field]
        p.save() # this will update only

        return HttpResponseRedirect(reverse("classe_post", args=[x[0], x[1]]))


@login_required
def edit(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))

    type_of_user = aluno_ou_prof(pk)

    DONO = True
    if pk != request.user.id:
        DONO = False
        return render(request, "eduworld/edit.html", {"DONO":DONO})

    if type_of_user == 'student':
        gerais = Aluno.objects.filter(usuario=pk).values()

    elif type_of_user == 'prof':
        gerais = Teacher.objects.filter(usuario=pk).values()
    else:
        return render(request, "eduworld/profile.html", {"NOT_FOUND":True})

    comps = Complementos.objects.filter(usuario=pk).values()
    form = imagem

    if request.method == "POST":
        if request.POST.get("salvar"):
            firstname = request.POST["first_name"]
            lastname = request.POST["last_name"]
            bio = request.POST["bio"]

            if type_of_user == 'student':
                school = request.POST["school"]
                education = request.POST["education"]

                p = Aluno.objects.get(usuario=pk)
                p.name = firstname  # change field]
                p.last_name = lastname  # change field
                p.school = school  # change field
                p.level = education  # change field
                p.save() # this will update only

            else:
                titulo = request.POST["titulo"]

                p = Teacher.objects.get(usuario=pk)
                p.name = firstname  # change field]
                p.last_name = lastname  # change field
                p.call = titulo  # change field
                p.save() # this will update only

            p = Complementos.objects.get(usuario=pk)
            p.bio = bio
            p.save()
            message = "Changes made successfully!"
            return render(request, "eduworld/edit.html", {"DONO":DONO, "type_of_user":type_of_user, "gerais":gerais,
                                                          "comps":comps, "message":message, "tipo":"success", "loc":comps[0]['foto']})

        if request.POST.get("salvarimagem"):
            form = request.FILES["updateimagem"]
            p = Complementos.objects.get(usuario=pk)
            p.foto = form
            p.save()
            message = "Picture successfully updated!"
            return render(request, "eduworld/edit.html", {"DONO":DONO, "type_of_user":type_of_user, "gerais":gerais,
                                                          "comps":comps, "message":message, "tipo":"success", "loc":comps[0]['foto']})

    return render(request, "eduworld/edit.html", {"DONO":DONO, "type_of_user":type_of_user, "gerais":gerais, "comps":comps,
                                                    "loc":comps[0]['foto']})

@login_required
def editclass(request, pk):
    if not is_complete(request.user.id):
        return HttpResponseRedirect(reverse("complete", args=[request.user.id]))

    type_of_user = aluno_ou_prof(request.user.id)

    if type_of_user != 'prof':
        return render(request, "eduworld/editclass.html", {'DONO':False})

    DONO = False
    classe = Classe.objects.filter(id=pk).values()
    dono = classe[0]['dono_id']
    if int(dono) == request.user.id:
        DONO = True

    if request.method == "POST":
        classname = request.POST["classname"]
        Room = request.POST["Room"]
        Subject = request.POST["Subject"]

        p = Classe.objects.get(id=pk)
        p.name = classname  # change field]
        p.subject = Subject  # change field
        p.room = Room  # change field
        p.save() # this will update only
        return HttpResponseRedirect(reverse("classroom", args=[pk]))


    return render(request, "eduworld/editclass.html", {"DONO":DONO, "data":classe, "pk":pk})


