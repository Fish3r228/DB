import psycopg2
from src.config import DB_CONFIG
from typing import List, Tuple, Optional

class DBManager:
    """
    Класс для управления запросами к базе данных PostgreSQL.
    """

    def __init__(self):
        """
        Инициализирует соединение с БД.
        """
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id)
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает все вакансии с названиями компаний, зарплатами и ссылками.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """
        Вычисляет среднюю зарплату по всем вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(COALESCE((salary_from + salary_to)/2, salary_from, salary_to))
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, Optional[int], Optional[int], str]]:
        """
        Возвращает вакансии с зарплатой выше средней.
        """
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE COALESCE((salary_from + salary_to)/2, salary_from, salary_to) > %s
            """, (avg,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, Optional[int], Optional[int], str]]:
        """
        Ищет вакансии по ключевому слову в названии.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE name ILIKE %s
            """, (f"%{keyword}%",))
            return cur.fetchall()
#