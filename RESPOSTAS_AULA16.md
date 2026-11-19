# Respostas - Aula 16

## Parte 1 - Questoes teoricas

1. `render()` combina um template com um contexto e devolve uma pagina HTML, portanto a URL normalmente representa uma pagina da interface web. `JsonResponse()` devolve dados serializados em JSON e e usado por endpoints ou APIs; a URL representa um recurso acessado por requisições HTTP.
2. `safe=False` permite que `JsonResponse` serialize objetos que nao sao dict, como listas e tuples. E necessario ao devolver `list(...)`, como em `JsonResponse(dados, safe=False)`.
3. `ModelForm` gera um formulario vinculado a um Model e valida dados destinados a paginas Django. `ModelSerializer` faz o mesmo tipo de automacao para dados da API REST: mapeia campos do Model, converte JSON/dict e valida dados de entrada.
4. `ListCreateAPIView` implementa GET para listar a colecao e POST para criar um recurso. `RetrieveUpdateDestroyAPIView` implementa GET para consultar um item, PUT para substituir seus dados, PATCH para alterar parcialmente e DELETE para excluir o item.
5. O servidor gera um Token associado ao usuario. A partir dele, o cliente envia o cabeçalho `Authorization: Token <valor>` em cada requisicao. A autenticacao nao depende de sessao ou estado armazenado no servidor, por isso se relaciona com Stateless: cada requisicao leva as credenciais necessarias e o servidor nao cria uma sessao de usuario para a API.

## Parte 2 - Complete o comando

a) `pip install djangorestframework`

b)
```python
class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'
```

c) `AlunoListCreateView(ListCreateAPIView)`

d) `AlunoDetailView(RetrieveUpdateDestroyAPIView)`

e)
```python
path('alunos/', AlunoListCreateView.as_view(), name='aluno-list-create')
```

f) `201 Created`

## Parte 3 - Encontre o erro

### Cenario A
`JsonResponse()` aceita dict por padrao e a chamada devolve uma lista, por isso ocorre `TypeError`. A correcao e converter a consulta para lista e usar `safe=False`:
```python
alunos = list(Aluno.objects.values())
return JsonResponse(alunos, safe=False)
```

### Cenario B
Faltam autenticacao e permissao padrao no `settings.py`. A configuracao minima e:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Tambem devem ser adicionados `rest_framework` e `rest_framework.authtoken` ao `INSTALLED_APPS`, e a rota de login deve usar `obtain_auth_token`.

## Parte 4 - Desafio extra
Um `ViewSet` agrupa em uma unica classe as operacoes de colecao e item, e o `DefaultRouter` registra automaticamente as rotas. Ele poderia substituir `AlunoListCreateView` e `AlunoDetailView`, expondo listar/criar em `/alunos/` e recuperar/atualizar/excluir em `/alunos/<pk>/` sem configurar manualmente duas classes genericas e dois `path()`.
