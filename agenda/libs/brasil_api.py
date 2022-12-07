from datetime import date
import requests, json    
import logging

from django.conf import settings
    
def is_feriado(data: date) -> bool:   
    logging.info(f'Fazendo requisição para BrasilAPI para a data: {date.isoformat()}') 
    if settings.TESTING == True:
        logging.info(f'Requisação não está sendo feita pois TESTING == True')
        if date.day == 25 and date.month == 12:
            return True
        return False
    
    ano = data.year
    request = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{ano}')
    if not request.status_code == 200:
        logging.error('Algum erro ocorreu na Brasil API')
        return False
        
    feriados = json.loads(request.text)
    for feriado in feriados:
        data_feriado_string = feriado['date'] 
        data_feriado = date.fromisoformat(data_feriado_string)
        if data == data_feriado:
            return True
    return False
    