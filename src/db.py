import psycopg2
from config import DB_CONFIG

def create_tables():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    hh_id INT UNIQUE,
                    name VARCHAR(255),
                    description TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    hh_id VARCHAR(50) UNIQUE,
                    company_id INT REFERENCES companies(id),
                    name VARCHAR(255),
                    salary_from INT,
                    salary_to INT,
                    url TEXT
                );
            """)
        conn.commit()

def insert_company(company):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO companies (hh_id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (hh_id) DO NOTHING
                RETURNING id
            """, (company["id"], company["name"], company.get("description")))
            result = cur.fetchone()
            return result[0] if result else None

def insert_vacancies(vacancies, company_id):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for vacancy in vacancies:
                salary = vacancy.get("salary", {})
                cur.execute("""
                    INSERT INTO vacancies (hh_id, company_id, name, salary_from, salary_to, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (hh_id) DO NOTHING
                """, (
                    vacancy["id"],
                    company_id,
                    vacancy["name"],
                    salary.get("from"),
                    salary.get("to"),
                    vacancy["alternate_url"]
                ))
        conn.commit()
# db con