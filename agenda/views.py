from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework import mixins, generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset
    
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer     

@api_view()
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
        
#    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
#    return JsonResponse(horarios_disponiveis)