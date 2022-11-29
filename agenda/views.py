from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework import mixins, generics, permissions
from django.contrib.auth.models import User

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer

class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'GET':
            return True
        username = request.query_params.get('username', None)
        if request.user.username == username:
            True
        return False

class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False

class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Agendamento.objects.filter(prestador__username=username)

    
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer  
    permission_classes = [IsPrestador]   

class PrestadorList(generics.ListAPIView):
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()

@api_view()
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
        
#    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
#    return JsonResponse(horarios_disponiveis)