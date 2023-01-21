from django.contrib import admin
from .models import User, Aluno, Teacher, Classe, ForumPost, ReplyForumComments
from .models import  Complementos, Gadgets, ClassePosts, ReplyPosts, PDFAssignments, StatusAluno, PrivateComments, ReplyPrivateComments
# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Aluno)
admin.site.register(Classe)
admin.site.register(Complementos)
admin.site.register(Gadgets)
admin.site.register(ClassePosts)
admin.site.register(ReplyPosts)
admin.site.register(PDFAssignments)
admin.site.register(StatusAluno)
admin.site.register(PrivateComments)
admin.site.register(ReplyPrivateComments)
admin.site.register(ForumPost)
admin.site.register(ReplyForumComments)

