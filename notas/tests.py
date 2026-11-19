from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Aluno


class AlunoAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste_api',
            password='Teste@123',
        )
        self.token = Token.objects.create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

    def test_sem_token_e_bloqueado(self):
        response = self.client.get('/alunos/')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_login_obtem_token(self):
        response = self.client.post(
            '/api/login/',
            {'username': 'teste_api', 'password': 'Teste@123'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_operacoes_crud(self):
        created = self.client.post(
            '/alunos/',
            {'nome': 'Ana', 'nota': '8.50'},
            format='json',
            **self.headers,
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        aluno_id = created.data['id']

        listed = self.client.get('/alunos/', **self.headers)
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 1)

        detail = self.client.get(f'/alunos/{aluno_id}/', **self.headers)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

        put = self.client.put(
            f'/alunos/{aluno_id}/',
            {'nome': 'Ana Silva', 'nota': '9.25'},
            format='json',
            **self.headers,
        )
        self.assertEqual(put.status_code, status.HTTP_200_OK)

        patch = self.client.patch(
            f'/alunos/{aluno_id}/',
            {'nota': '9.75'},
            format='json',
            **self.headers,
        )
        self.assertEqual(patch.status_code, status.HTTP_200_OK)

        deleted = self.client.delete(f'/alunos/{aluno_id}/', **self.headers)
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Aluno.objects.filter(pk=aluno_id).exists())

    def test_view_json_response(self):
        Aluno.objects.create(nome='Bruno', nota='7.50')
        response = self.client.get('/alunos-json/', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['nome'], 'Bruno')
