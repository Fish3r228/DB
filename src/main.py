from config import EMPLOYER_IDS
from hh_api import get_employer_info, get_vacancies
from db import create_tables, insert_company, insert_vacancies
from db_manager import DBManager

def main():
    create_tables()

    for emp_id in EMPLOYER_IDS:
        employer = get_employer_info(emp_id)
        if employer:
            print(f"Загружается работодатель: {employer['name']}")
            company_id = insert_company(employer)
            if company_id:
                vacancies = get_vacancies(emp_id)
                insert_vacancies(vacancies, company_id)

    db = DBManager()
    print("Компании и количество вакансий:")
    for row in db.get_companies_and_vacancies_count():
        print(row)

    print("\nВакансии с выше средней зарплатой:")
    for row in db.get_vacancies_with_higher_salary():
        print(row)

    print("\nПоиск по ключевому слову 'Python':")
    for row in db.get_vacancies_with_keyword("Python"):
        print(row)

if __name__ == '__main__':
    main()
#main.