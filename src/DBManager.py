import psycopg2
from config import config  # импортируем функцию из config.py

class DBManager:
    def __init__(self, config_file="database.ini", config_section="postgresql"):
        self.params = config(config_file, config_section)

    def _execute_query(self, query: str, params: tuple = None) -> list:
        """Вспомогательный метод для выполнения SQL‑запросов с автоматическим управлением соединением."""
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()


    def get_companies_and_vacancies_count(self) -> list:
        conn = psycopg2.connect(dbname='my_hh_db', **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT
                employers.name AS "company_name",
                employers.open_vacancies AS "open_vacancies"
            FROM
                employers
        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_all_vacancies(self) -> list:
        conn = psycopg2.connect(dbname='my_hh_db', **self.params)

        cur = conn.cursor()
        cur.execute("""
                            SELECT employers.name as "company_name",
                            vacancies.name as "vacancies_name",
                            vacancies.salary as "salary",
                            vacancies.url as "url"
                            FROM
                            employers
                            JOIN vacancies
                            ON vacancies.employer_id = employers.employer_id
                        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_avg_salary(self) -> list:
        conn = psycopg2.connect(dbname='my_hh_db', **self.params)

        cur = conn.cursor()
        cur.execute("""
                            SELECT AVG(salary) AS avg_salary
                            FROM vacancies
                        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_vacancies_with_higher_salary(self) -> list:
        conn = psycopg2.connect(dbname='my_hh_db', **self.params)
        cur = conn.cursor()
        cur.execute("""
                            SELECT vacancies.name as "vacancies_name"
                            FROM vacancies
                            WHERE salary > (
                            SELECT AVG(salary)
                            FROM vacancies
                            WHERE salary IS NOT NULL
                            )
                        """)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results


    def get_vacancies_with_keyword(self, keyword: str) -> list:
        conn = psycopg2.connect(dbname='my_hh_db', **self.params)
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT * FROM vacancies WHERE name ILIKE %s",
                (f"%{keyword}%",)
            )
            results = cur.fetchall()

            if not results:
                print(f"По запросу '{keyword}' вакансий не найдено.")
            else:
                print(f"Найдено {len(results)} вакансий по запросу '{keyword}'.")

            return results
        finally:
            cur.close()
            conn.close()
