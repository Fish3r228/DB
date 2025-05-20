import pytest
from unittest.mock import patch, MagicMock
from src.db_manager import DBManager

@pytest.fixture
def mock_db_connection():
    """
    Фикстура для мока соединения с базой данных PostgreSQL.
    Подменяет psycopg2.connect и возвращает мок-объект курсора.
    """
    with patch("src.db_manager.psycopg2.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        yield mock_cursor

def test_get_companies_and_vacancies_count(mock_db_connection):
    """
    Тестирует метод get_companies_and_vacancies_count().
    Проверяет корректность возвращаемых данных о количестве вакансий по компаниям.
    """
    mock_db_connection.fetchall.return_value = [("Company A", 5), ("Company B", 3)]
    db = DBManager()
    result = db.get_companies_and_vacancies_count()
    assert result == [("Company A", 5), ("Company B", 3)]

def test_get_all_vacancies(mock_db_connection):
    """
    Тестирует метод get_all_vacancies().
    Проверяет, что возвращаются все вакансии с нужными полями.
    """
    mock_db_connection.fetchall.return_value = [
        ("Company A", "Vacancy 1", 50000, 70000, "https://hh.ru/v1"),
        ("Company B", "Vacancy 2", None, 80000, "https://hh.ru/v2"),
    ]
    db = DBManager()
    result = db.get_all_vacancies()
    assert len(result) == 2
    assert result[0][0] == "Company A"

def test_get_avg_salary(mock_db_connection):
    """
    Тестирует метод get_avg_salary().
    Проверяет, что средняя зарплата возвращается корректно.
    """
    mock_db_connection.fetchone.return_value = [75000]
    db = DBManager()
    result = db.get_avg_salary()
    assert result == 75000

def test_get_vacancies_with_higher_salary(mock_db_connection):
    """
    Тестирует метод get_vacancies_with_higher_salary().
    Подменяет метод get_avg_salary и проверяет выборку вакансий с зарплатой выше средней.
    """
    mock_db_connection.fetchall.return_value = [
        ("Vacancy 1", 80000, 90000, "https://hh.ru/v1")
    ]
    with patch.object(DBManager, "get_avg_salary", return_value=70000):
        db = DBManager()
        result = db.get_vacancies_with_higher_salary()
        assert result[0][0] == "Vacancy 1"

def test_get_vacancies_with_keyword(mock_db_connection):
    """
    Тестирует метод get_vacancies_with_keyword().
    Проверяет, что возвращаются вакансии, содержащие ключевое слово в названии.
    """
    mock_db_connection.fetchall.return_value = [
        ("Python Developer", 60000, 80000, "https://hh.ru/v123")
    ]
    db = DBManager()
    result = db.get_vacancies_with_keyword("Python")
    assert "Python" in result[0][0]
#
