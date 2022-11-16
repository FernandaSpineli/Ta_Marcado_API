import json
from rest_framework.test import APITestCase

# Create your tests here.
class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/agendamentos/')
        data = json.loads(response.content)
        self.assertEqual(data, [])
        
        # json.dumps => transforma de python para json
        # json.loads => trasforma de json para python