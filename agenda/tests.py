from datetime import datetime, timezone
import json

from rest_framework.test import APITestCase

from agenda.models import Agendamento

# Create your tests here.

class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/agendamentos/')
        data = json.loads(response.content)
        self.assertEqual(data, [])
        
        # json.dumps => transforma de python para json
        # json.loads => trasforma de json para python
    
    def test_listagem_de_agedamentos_criados(self):
        Agendamento.objects.create(
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
            'telefone_cliente': '(11) 99343-1524'
        }
        
        response = self.client.get('/api/agendamentos/')
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)
    
class TestAgendamentoDetail(APITestCase):
    def test_cria_agendamento(self):
        novo_agendamento = {
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
            'telefone_cliente': '99343-1524'
        }
        response = self.client.post('/api/agendamentos/', novo_agendamento, format='json')
        buscar_agendamento = Agendamento.objects.get()
        self.assertEqual(buscar_agendamento.data_horario, datetime(2022, 12, 25, 12, 30, 00, tzinfo=timezone.utc))
    
    def test_quando_request_e_invalido_retorna_400(self):
        novo_agendamento = {
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
        }
        response = self.client.post('/api/agendamentos/', novo_agendamento, format='json')
        self.assertEqual(response.status_code, 400)

    def test_deleção_de_agendamento(self):
        Agendamento.objects.create(
            data_horario=datetime(2022, 12, 24, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com.br',
            telefone_cliente='(11) 99343-1524'       
        )
        response = self.client.delete('/api/agendamentos/1/')
        self.assertEqual(response.status_code, 204)
        
    def testar_atualizacao_de_agendamento(self):
        Agendamento.objects.create(
            data_horario=datetime(2022, 12, 24, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com.br',
            telefone_cliente='(11) 99343-1524'       
        )
        agendamento_atualizado = {
            'data_horario': '2022-12-25T12:30:00Z',
            'nome_cliente': 'AliceSpineli',
            'email_cliente': 'alice2@gmail.com.br',
            'telefone_cliente': '99343-1524'
        }
        response = self.client.patch('/api/agendamentos/1/', agendamento_atualizado, format='json')
        self.assertEqual(response.status_code, 200)