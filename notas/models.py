from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    nota = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.nome
