from src.api import HH_vacancies


class Vacancy:
    "Класс для работы с вакансиями"

    __slots__ = ("name", "_salary", "url", "responsibility", "employer_id")

    def __init__(
        self,
        name: str,
        salary: dict[str, None | int] | None,
        url: str,
        responsibility: str,
        employer_id: int,
    ) -> None:
        self.name = name
        self.salary = salary
        self.url = url
        self.responsibility = responsibility
        self.employer_id = employer_id

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: dict[str, None | int] | None) -> None:
        "Валидация данных по зарплате"
        """
        Ожидается словарь формата:
        {
            "from": int | None,
            "to": int | None
        }

        Логика:
        - если есть from и to → берём среднее
        - если есть только from → берём from
        - если есть только to → берём to
        - если данных нет или они некорректны → 0
        """

        if not isinstance(value, dict):
            self._salary = 0
            return

        salary_from = value.get("from")
        salary_to = value.get("to")

        if isinstance(salary_from, int) and isinstance(salary_to, int):
            self._salary = (salary_from + salary_to) / 2
        elif isinstance(salary_from, int):
            self._salary = float(salary_from)
        elif isinstance(salary_to, int):
            self._salary = float(salary_to)
        else:
            self._salary = 0

    def __eq__(self, other: object) -> bool:
        "Проверяет равенство двух объектов Vacancy по зарплате"
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __gt__(self, other: object) -> bool:
        "Проверяет больше ли зарплата текущего объекта Vacancy по зарплате"
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __lt__(self, other: object) -> bool:
        "Проверяет меньше ли зарплата текущего объекта Vacancy по зарплате"
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def vacancies_cast_to_dict(self) -> dict[str, (str | float)]:
        "Перевод данных в словарь"
        return {"name": self.name, "salary": self.salary, "url": self.url, "responsibility": self.responsibility, "employer_id": self.employer_id}