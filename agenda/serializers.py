from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User

from agenda.models import Agendamento

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
        
    def validate(self, attrs):
        telefone_cliente = attrs.get('telefone_cliente', '')
        email_cliente = attrs.get('email_cliente', '')
        
        if email_cliente.endswith('.br') and telefone_cliente.startswith('+') and not telefone_cliente.startswith('+55'):
            raise serializers.ValidationError('E-mail brasileiro deve estarassociado a um número do Brasil (+55)')
        return attrs
    