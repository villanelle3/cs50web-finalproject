from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("joinclass", views.joinclass, name="joinclass"),
    path("createclass", views.createclass, name="createclass"),
    path("complete/<int:pk>", views.complete, name="complete"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("classroom/<int:pk>", views.classroom, name="classroom"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("assignment/<int:pk>", views.assignment, name="assignment"),
    path("newassignment/<int:pk>", views.newassignment, name="newassignment"),
    path("editclass/<int:pk>", views.editclass, name="editclass"),
    path("remove/<int:classid>/<int:alunoid>", views.aluno_delete, name="aluno_delete"),
    path("classroom/<int:classid>/post/<int:pk>", views.classe_post, name="classe_post"),
    path("addcomment", views.addcomment, name="addcomment"),
    path("editcomment", views.edit_data, name="editcomment"),
    path("edittitulo", views.edittitulo, name="edittitulo"),
    path("replycomment", views.reply_coment, name="replycomment"),
    path("addnewcomment", views.add_data, name="addnewcomment"),
    path("addlike", views.add_like, name="addlike"),
    path("editassignm", views.editar_data, name="editassignm"),
    path("newformreply/<int:pk>", views.newformreply, name="newformreply"),
    path("deletereply", views.deletereply, name="deletereply"),
    path("deletepost/<int:pk>/<int:classid>", views.deletepost, name="deletepost"),
    path("newhomework/<int:pk>", views.create_homework, name="createhomework"),
    path("cancel/<int:pk>", views.cancel, name="cancel"),
    path("search", views.search, name="search"),
    path("forum", views.forum_index, name="forum"),
    path("filter-form-data", views.forum_filter, name="filter-form-data"),
    path("forum/question/<int:pk>", views.forum_question, name="forumquestion"),
]



