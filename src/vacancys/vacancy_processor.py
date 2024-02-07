import validators

from src.apis.hh_api import HeadHunterAPI


class VacancyProcessor:

    def __init__(self, **kwargs) -> None:
        self.__vacancy_id = kwargs["vacancy_id"]
        self.__vacancy_name = kwargs["vacancy_name"]
        self.__salary_from = kwargs["salary_from"]
        self.__salary_to = kwargs["salary_to"]
        self.__vacancy_url = kwargs["vacancy_url"]
        self.__city = kwargs["city"]
        self.__experience = kwargs["experience"]
        self.__employer = kwargs["employer"]

    @property
    def vacancy_id(self):
        return self.__vacancy_id

    @property
    def vacancy_name(self):
        return self.__vacancy_name

    @property
    def salary_from(self):
        return self.__salary_from

    @salary_from.setter
    def salary_from(self, value):
        if isinstance(value, int):
            self.__salary_from = value
        else:
            self.__salary_from = 0

    @property
    def salary_to(self):
        return self.__salary_to

    @salary_to.setter
    def salary_to(self, value):
        if isinstance(value, int):
            self.__salary_to = value
        else:
            self.__salary_to = self.__salary_from

    @property
    def check_salary(self):
        if self.__salary_from and not self.salary_to:
            return f"Зарплатная вилка от {self.salary_from}"
        elif not self.__salary_from and self.salary_to:
            return f"Зарплатная вилка до {self.salary_to}"
        elif self.__salary_from and self.salary_to:
            return f"Зарплатная вилка от {self.salary_from} до {self.salary_to}"
        else:
            return f"Зарплата не указана"

    @property
    def vacancy_url(self):
        return self.__vacancy_url

    @vacancy_url.setter
    def vacancy_url(self, url):
        if not validators.url(url):
            self.__vacancy_url = "https://hh.ru/vacancy/"
        else:
            self.__vacancy_url = url

    @property
    def city(self):
        return self.__city

    @property
    def experience(self):
        return self.__experience

    @property
    def employer(self):
        return self.__employer

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.vacancy_id}, "
            f"{self.vacancy_name}, {self.salary_from}, "
            f"{self.salary_to}, {self.__city}, "
            f"{self.__experience}, {self.__employer})"
        )

    def __str__(self) -> str:
        return (
            f"Название вакансии - {self.vacancy_name}\n"
            f"{self.check_salary}\n"
            f"Требуемый опыт {self.experience}\n"
            f"Наименование организации - {self.__employer}\n"
            f"Город расположения - {self.__city}\n"
            f"Ссылка на вакансию - {self.__vacancy_url}\n"
        )

    def __gt__(self, other) -> bool:
        if self.salary_from:
            return self.salary_from > other.salary_from
        elif self.salary_to:
            return self.salary_to > other.salary_to


# it's necessary to transfer data from the user
hh = HeadHunterAPI("Москва", "python", 1, 150000)

vacancies_list = hh.get_vacancies()
vacancies_obj = []

for vacancy in vacancies_list:
    vp = VacancyProcessor(**vacancy)
    vacancies_obj.append(vp)
