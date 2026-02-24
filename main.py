import os

import psycopg2

from src.DBManager import DBManager
from src.api import HH_vacancies
from src.data_base import create_database, save_data_to_database
from src.employers import Employer
from src.utils import get_list_employers, get_list_vacancies
from config import config
from src.vacancies import Vacancy


def main():


    list_id_employers = [2573503, 3847149, 2184551, 1386452, 2180726, 238661, 629945, 9855, 2597277, 3714350]

    list_employers = get_list_employers(list_id_employers)

    employers = []
    for emp in list_employers:
        # Создаём объект Employer и добавляем его в список vacancies
        employer = Employer(
            employer_id=int(emp['id']),
            name=emp['name'],
            url=emp['alternate_url'],
            open_vacancies=emp['open_vacancies']
        )
        employers.append(employer)

    employers_dict = []
    for emp in employers:
        employers_dict.append(emp.employers_cast_to_dict())



    list_vacancies = get_list_vacancies(list_id_employers)

    vacancies = []
    for vac in list_vacancies:
        # Создаём объект Vacancy и добавляем его в список vacancies
        vacancy = Vacancy(
            employer_id=int(vac['employer']['id']),
            name=vac['name'],
            salary=vac['salary'],
            url=vac['alternate_url'],
            responsibility=vac['snippet']['responsibility']
        )
        vacancies.append(vacancy)

    sorted_dict = sorted(vacancies, reverse=True)

    vacancies_dict = []
    for vac in sorted_dict:
        # Переводим объект Vacancy в словарь и добавляем его в список vacancies_dict
        vacancies_dict.append(vac.vacancies_cast_to_dict())

    params = config()

    create_database('my_hh_db', params)
    save_data_to_database(employers_dict, vacancies_dict, 'my_hh_db', params)


print("Привет! Добро пожаловать в программу работы с вакансиями")
print(
    "Выберите необходимый пункт меню:\n"
    "1. Получить список всех компаний и количество вакансий у каждой компании\n"
    "2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
    "3. Получить среднюю зарплату по вакансиям\n"
    "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
    "5. Получить список всех вакансий, в названии которых содержится переданное слово\n"
)

try:
    num_menu = int(input("Введите номер пункта меню: "))
    a = DBManager()  # Передаём параметры подключения

    if num_menu == 1:
        print("Получаем список всех компаний и количество вакансий у каждой компании.\n")
        results = a.get_companies_and_vacancies_count()
        print(results)

    elif num_menu == 2:
        print("Получаем список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.\n")
        results = a.get_all_vacancies()
        print(results)

    elif num_menu == 3:
        print("Получаем среднюю зарплату по вакансиям.\n")
        avg_salary = a.get_avg_salary()
        print(avg_salary)

    elif num_menu == 4:
        print("Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n")
        results = a.get_vacancies_with_higher_salary()
        print(results)

    elif num_menu == 5:
        keyword = input("Введите ключевое слово для поиска вакансий: ").strip()
        if not keyword:
            print("Ошибка: ключевое слово не может быть пустым.")
        else:
            print(f"Выполняется поиск по запросу: '{keyword}'")
            print(f"Получаем список всех вакансий, в названии которых содержится слово '{keyword}'\n")
            results = a.get_vacancies_with_keyword(keyword)
            if results:
                print(results)
            else:
                print(f"По запросу '{keyword}' вакансий не найдено.")
    else:
        print("Ошибка: неверный номер пункта меню. Пожалуйста, выберите число от 1 до 5.")

except ValueError:
    print("Ошибка: пожалуйста, введите целое число.")
except psycopg2.OperationalError as e:
    print(f"Ошибка подключения к базе данных: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")





if __name__ == '__main__':
    main()