from typing import Iterable
from datetime import date, datetime, timedelta, timezone
import requests

from agenda.models import Agendamento
from agenda.libs import brasil_api

def get_horarios_disponiveis(data:date) -> Iterable[datetime]:
    try:
        if brasil_api.is_feriado(data):
            return []
    except ValueError:
        ...
        
    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc) 
    delta = timedelta(minutes=30)
    horarios_disponiveis = set()
    while start < end:
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.add(start)
        start = start + delta
        
    return horarios_disponiveis