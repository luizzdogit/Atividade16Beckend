from django.urls import path

from .views import AlunoDetailView, AlunoListCreateView, lista_alunos

urlpatterns = [
    path('alunos-json/', lista_alunos, name='lista-alunos-json'),
    path('alunos/', AlunoListCreateView.as_view(), name='aluno-list-create'),
    path('alunos/<int:pk>/', AlunoDetailView.as_view(), name='aluno-detail'),
]
