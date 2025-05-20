"""
HH.ru Vacancies Project
========================
Загрузка данных о компаниях и вакансиях с hh.ru и работа с PostgreSQL БД через psycopg2.
"""

# config.py
DB_CONFIG = {
    'dbname': 'your_db_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost'
}

EMPLOYER_IDS = [1740, 3529, 78638, 15478, 80, 2180, 3776, 1122462, 1122462, 84585]
#