from datetime import datetime, timezone
import json

from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from agenda.models import Agendamento

# Create your tests here.

class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        self.client.login(username='nanda', password='123')
        response = self.client.get('/api/agendamentos/?username=fernanda')
        data = json.loads(response.content)
        self.assertEqual(data, [])
        # json.dumps => transforma de python para json
        # json.loads => trasforma de json para python
    
    def test_listagem_de_agedamentos_criados(self):
        nanda = User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        self.client.login(username='nanda', password='123')
        Agendamento.objects.create(
            prestador = nanda,
            data_horario=datetime(2022, 12, 24, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com.br',
            telefone_cliente='(11) 99343-1524'       
        )
        agendamento_serializado = {
            'id': 1,
            'data_horario': '2022-12-24T00:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com.br',
            'telefone_cliente': '(11) 99343-1524',
            'prestador': 'nanda'
        }
        
        response = self.client.get('/api/agendamentos/')
        self.assertEqual(response.status_code, 200)
    
class TestAgendamentoDetail(APITestCase):
    def test_cria_agendamento(self):
        nanda = User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        novo_agendamento = {
            'prestador': 'nanda',
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
            'telefone_cliente': '99343-1524'
        }
        response = self.client.post('/api/agendamentos/', novo_agendamento, format='json')
        self.assertEqual(response.status_code, 201)
        
        buscar_agendamento = Agendamento.objects.get()
        self.assertEqual(buscar_agendamento.data_horario, datetime(2022, 12, 25, 12, 30, 00, tzinfo=timezone.utc))
    
    def test_quando_request_e_invalido_retorna_400(self):
        User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        self.client.login(username='nanda', password='123')
        novo_agendamento = {
            'prestador': 'nanda',
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
        }
        response = self.client.post('/api/agendamentos/', novo_agendamento, format='json')
        self.assertEqual(response.status_code, 400)

    def test_deleção_de_agendamento(self):
        nanda = User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        self.client.login(username='nanda', password='123')
        Agendamento.objects.create(
            prestador = nanda,
            data_horario=datetime(2022, 12, 24, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com.br',
            telefone_cliente='(11) 99343-1524'       
        )
        response = self.client.delete('/api/agendamentos/1/')
        self.assertEqual(response.status_code, 204)
        
    def testar_atualizacao_de_agendamento(self):
        nanda = User.objects.create_user(email='nanda@gmail.com', username='nanda', password='123')
        self.client.login(username='nanda', password='123')
        Agendamento.objects.create(
            prestador = nanda,
            data_horario=datetime(2022, 12, 24, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com.br',
            telefone_cliente='(11) 99343-1524'       
        )
        agendamento_atualizado = {
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
            'telefone_cliente': '99343-1524',
            'prestador': 'nanda'
        }
        response = self.client.patch('/api/agendamentos/1/', agendamento_atualizado, format='json')
        self.assertEqual(response.status_code, 200)
        
class TestGetHorarios(APITestCase):
    def test_quando_data_e_feriado_retorna_lista_vazia(self):
        response = self.client.get('/api/horarios/?data=2022-12-25')
        #self.assertEqual(response.content, [])
        self.assertEqual(response.status_code, 200)
        
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self):
        response = self.client.get('/api/horarios/?data=2022-10-25')
        self.assertEqual(response.status_code, 200)