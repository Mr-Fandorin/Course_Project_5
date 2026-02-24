class Employer:
    "Класс для работы с работодателями"

    __slots__ = ("employer_id", "name", "url", "open_vacancies")

    def __init__(
        self,
        employer_id: int,
        name: str,
        url: str,
        open_vacancies: int,
    ) -> None:
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.open_vacancies = open_vacancies


    def employers_cast_to_dict(self) -> dict[str, (str | int)]:
        "Перевод данных в словарь"
        return {"employer_id": self.employer_id, "name": self.name, "url": self.url, "open_vacancies": self.open_vacancies}