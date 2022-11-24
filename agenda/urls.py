from django.urls import path

from agenda.views import agendamento_detail, AgendamentoList

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:id>/', agendamento_detail)
]

