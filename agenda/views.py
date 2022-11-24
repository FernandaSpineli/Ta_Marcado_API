from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

class AgendamentoList(APIView):
    def get(self, request):
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request):
        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class AgendamentoDetail(APIView):
    def get(self, request):
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)
    def patch(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
    def delete(self, request, id):
        obj = get_object_or_404(Agendamento, id=id)
        obj.delete()
        return Response(status=204)
    

@api_view()
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
        
#    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
#    return JsonResponse(horarios_disponiveis)