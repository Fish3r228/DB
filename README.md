# HH.ru Vacancies Database Project

## 📌 Описание

Проект предназначен для получения данных о работодателях и вакансиях с сайта [hh.ru](https://hh.ru) через публичный API, сохранения этих данных в базу данных PostgreSQL и предоставления удобных методов доступа через Python-класс `DBManager`.

Проект выполняется с использованием библиотек `requests` для работы с API hh.ru и `psycopg2` для взаимодействия с PostgreSQL.

## 🛠️ Функциональность:

- Получение данных о 10 популярных работодателях.
- Загрузка вакансий по каждой компании.
- Создание и наполнение базы данных.
- Класс `DBManager` для запросов:
  - Получение всех компаний и количества их вакансий.
  - Получение всех вакансий.
  - Подсчет средней зарплаты.
  - Поиск вакансий с зарплатой выше средней.
  - Поиск вакансий по ключевому слову.

## 📂 Структура проекта
hh_project/
│
├── config.py # Конфигурация подключения и ID работодателей
├── hh_api.py # Функции для работы с API hh.ru
├── db.py # Создание таблиц и загрузка данных в БД
├── db_manager.py # Класс DBManager с методами запросов
├── main.py # Основной скрипт
├── requirements.txt # Зависимости проекта
└── README.md # Документация проекта


## 🏢 Используемые работодатели (hh.ru ID)

1. Яндекс — `1740`  
2. Сбербанк — `3529`  
3. Тинькофф — `78638`  
4. VK — `15478`  
5. Альфа-Банк — `80`  
6. Ozon — `2180`  
7. МТС — `3776`  
8. Skyeng — `1122462`  
9. Самокат — `1122462`  
10. Авито — `84585`

## 💻  Установка

1. Клонируйте репозиторий:

git clone https://github.com/your_username/hh_project.git
cd hh_project

2. Установка зависимостей : 
pip install -r requirements.txt

3. Настройте подключение к вашей базе данных PostgreSQL в config.py:
DB_CONFIG = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost'  # или другой адрес
}

4. Запуск:  
python main.py
5. Примеры работы с DBManager: 
db = DBManager()

db.get_companies_and_vacancies_count()
# → [('Яндекс', 50), ('Сбербанк', 45), ...]

db.get_all_vacancies()
# → [('Яндекс', 'Python Developer', 100000, 150000, 'https://hh.ru/vacancy/...'), ...]

db.get_avg_salary()
# → 125000.0

db.get_vacancies_with_higher_salary()
# → [('Senior Python Developer', 160000, 200000, 'https://hh.ru/...'), ...]

db.get_vacancies_with_keyword('Python')
# → [('Python Developer', 120000, 160000, 'https://hh.ru/...'), ...]
