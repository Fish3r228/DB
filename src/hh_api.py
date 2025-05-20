import requests
import time
from typing import Optional, List, Dict, Any

def get_employer_info(employer_id: int) -> Optional[Dict[str, Any]]:
    """
    Получает информацию о работодателе по ID.
    """
    response = requests.get(f'https://api.hh.ru/employers/{employer_id}')
    if response.status_code == 200:
        return response.json()
    return None

def get_vacancies(employer_id: int) -> List[Dict[str, Any]]:
    """
    Получает список всех вакансий от указанного работодателя.
    """
    vacancies = []
    page = 0
    while True:
        response = requests.get('https://api.hh.ru/vacancies', params={
            'employer_id': employer_id,
            'page': page,
            'per_page': 100
        })
        if response.status_code != 200:
            break
        data = response.json()
        vacancies.extend(data['items'])
        if page >= data['pages'] - 1:
            break
        page += 1
        time.sleep(0.2)
    return vacancies
#4