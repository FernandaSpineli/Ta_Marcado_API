from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework import mixins, generics

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoList(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    
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