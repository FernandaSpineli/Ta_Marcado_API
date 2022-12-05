from datetime import date
import requests, json    

from django.conf import settings
    
def is_feriado(data: date) -> bool:    
    if settings.TESTING == True:
        if date.day == 25 and date.month == 12:
            return True
        return False
    
    ano = data.year
    request = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{ano}')
    if not request.status_code == 200:
        raise ValueError('Não foi possível consultar os feriados.')
    
    feriados = json.loads(request.text)
    for feriado in feriados:
        data_feriado_string = feriado['date'] 
        data_feriado = date.fromisoformat(data_feriado_string)
        if data == data_feriado:
            return True
    return False
    