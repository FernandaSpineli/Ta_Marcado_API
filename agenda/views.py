from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
    ):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class AgendamentoDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
    ):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)        

@api_view()
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
        
#    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
#    return JsonResponse(horarios_disponiveis)