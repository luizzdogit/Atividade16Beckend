from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Aluno
from .serializers import AlunoSerializer


def lista_alunos(request):
    alunos = list(Aluno.objects.values())
    return JsonResponse(alunos, safe=False)


class AlunoListCreateView(ListCreateAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class AlunoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
