from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User

from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
     
    prestador = serializers.CharField()
    def validate_prestador(self, value):
        try:
            prestador = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('username não existe.')
        return prestador
       
    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Agendamento não pode ser feito no passado.')
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError('Esse horário não está disponivel.')
        return value
     
    def validate(self, attrs):
        telefone_cliente = attrs.get('telefone_cliente', '')
        email_cliente = attrs.get('email_cliente', '')
        data = attrs.get('data_horario').date()
        if Agendamento.objects.filter(email_cliente=email_cliente, data_horario__date=data).exists():
            raise serializers.ValidationError('Já existe um agendamento para esse cliente nessa data.')
        
        if email_cliente.endswith('.br') and telefone_cliente.startswith('+') and not telefone_cliente.startswith('+55'):
            raise serializers.ValidationError('E-mail brasileiro deve estarassociado a um número do Brasil (+55)')
        return attrs
    
class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos']
        
    agendamentos = AgendamentoSerializer(many=True, read_only=True)
    