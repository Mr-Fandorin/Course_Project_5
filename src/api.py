import requests


class HH_employers:
    "Класс для загрузки Вакансий с HeadHunter"

    def __init__(self, employer_id: int) -> None:
        self.__url = f"https://api.hh.ru/employers/{employer_id}"
        # self.__employers = []

    def _api_connect(self, number: str) -> requests.Response:
        "Выполнение API запроса"
        response = requests.get(self.__url)
        if response.status_code != 200:
            raise ValueError("Failed to get info")
        return response

    def load_employers(self) -> list:
        "Получение Работодателя"
        employer = self._api_connect(self.__url).json()
        return employer



class HH_vacancies:
    """Класс для загрузки вакансий с HeadHunter"""

    def __init__(self, employer_id: int) -> None:
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__employer_id = employer_id
        self.__params = {
            "employer_id": employer_id,
            "page": 0,
            "per_page": 100,
            "only_with_salary": True,
            "currency": "RUR"
        }
        self.__vacancies = []

    def _api_connect(self) -> dict:
        """Выполнение API запроса"""
        response = requests.get(self.__base_url, params=self.__params)
        if response.status_code != 200:
            raise ValueError(f"Failed to get info for employer {self.__employer_id}: {response.status_code}")
        return response.json()

    def load_vacancies(self) -> list:
        """Получение вакансий с пагинацией"""
        while True:
            data = self._api_connect()
            vacancies_page = data.get("items", [])

            # Если страница пустая — заканчиваем
            if not vacancies_page:
                break

            self.__vacancies.extend(vacancies_page)

            # Проверяем, есть ли следующая страница
            current_page = self.__params["page"]
            total_pages = data.get("pages", 0)

            if current_page + 1 >= total_pages:
                break

            # Переходим к следующей странице
            self.__params["page"] += 1

        return self.__vacancies





if __name__ == "__main__":
    # a = HH_vacancies(2573503)
    # print(a.load_vacancies())

    a = HH_employers(2573503)
    print(a.load_employers())
