import psycopg2
from config import DB_CONFIG

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id)
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(COALESCE((salary_from + salary_to)/2, salary_from, salary_to))
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE COALESCE((salary_from + salary_to)/2, salary_from, salary_to) > %s
            """, (avg,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, salary_from, salary_to, url
                FROM vacancies
                WHERE name ILIKE %s
            """, (f"%{keyword}%",))
            return cur.fetchall()
#db mang