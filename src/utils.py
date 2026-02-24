from src.api import HH_employers, HH_vacancies


def get_list_employers(id_list_employers: list) -> list:
    employers = []
    for employer_id in id_list_employers:
        try:
            a = HH_employers(employer_id)
            employer_data = a.load_employers()
            employers.append(employer_data)
        except Exception as e:
            print(f"Ошибка при загрузке работодателя {employer_id}: {e}")
    return employers


def get_list_vacancies(id_list_employers: list) -> list:
    vacancies = []
    for employer_id in id_list_employers:
        try:
            a = HH_vacancies(employer_id)
            employer_vacancies = a.load_vacancies()
            vacancies.extend(employer_vacancies)
        except Exception as e:
            print(f"Ошибка при загрузке вакансий для {employer_id}: {e}")
    return vacancies


if __name__ == "__main__":


    list_vac = get_list_vacancies(
        [2573503, 3847149, 2184551, 1386452, 2180726, 238661, 629945, 9855, 2597277, 3714350]
    )
    print(list_vac)
