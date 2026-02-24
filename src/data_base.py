# Импортируйте библиотеку psycopg2
import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Проверяем, существует ли БД — если да, удаляем
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        if cur.fetchone():
            cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")
    except Exception as e:
        print(f"Ошибка при создании БД: {e}")
        raise
    finally:
        cur.close()
        conn.close()
    #
    # cur.close()
    # conn.close()


    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                url TEXT,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR NOT NULL,
                salary INTEGER,
                url TEXT,
                responsibility TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data_employers: list, data_vacancies: list, database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data_employers:

            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer['employer_id'], employer['name'], employer['url'],
                 employer['open_vacancies'])
            )
            # employer_id = cur.fetchone()[0]

        for vacancy in data_vacancies:

            cur.execute(
                """
                 INSERT INTO vacancies (employer_id, name, salary, url, responsibility)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (vacancy['employer_id'], vacancy['name'], vacancy['salary'],
                 vacancy['url'], vacancy.get('responsibility', ''))
            )

    conn.commit()
    conn.close()
