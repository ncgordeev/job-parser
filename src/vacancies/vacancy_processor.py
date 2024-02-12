import validators


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
        self.__value = 0
        self.__platform = kwargs["platform"]

    @property
    def vacancy_id(self):
        return self.__vacancy_id

    @property
    def vacancy_name(self):
        return self.__vacancy_name

    @property
    def salary_from(self):
        return self.__salary_from

    @property
    def salary_to(self):
        return self.__salary_to

    @property
    def value(self) -> int:
        if self.salary_from and self.salary_to:
            self.__value = (self.salary_from + self.salary_to) // 2
        elif self.salary_from and not self.salary_to:
            self.__value = self.salary_from
        elif not self.salary_from and self.salary_to:
            self.__value = self.salary_to
        return self.__value

    @property
    def check_salary(self):
        if self.__salary_from and not self.salary_to:
            return f"Зарплатная вилка от {self.salary_from}"
        elif not self.__salary_from and self.salary_to:
            return f"Зарплатная вилка до {self.salary_to}"
        elif self.__salary_from and self.salary_to:
            return f"Зарплатная вилка от {self.salary_from} до {self.salary_to}"
        else:
            return "Зарплата не указана"

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

    def has_salary(self):
        """
        Check if the vacancy has salary information.
        :return: True if salary information is available, False otherwise.
        """
        return self.__salary_from is not None or self.__salary_to is not None

    def is_salary_in_range(self, value_from, value_to):
        """
        Check if the salary of the vacancy is within the specified range.
        :param value_from: The lower bound of the salary range.
        :param value_to: The upper bound of the salary range.
        :return: True if the salary is within the range, False otherwise.
        """
        if not self.has_salary():
            return False

        start_salary = self.__salary_from or self.__salary_to
        end_salary = self.__salary_to or self.__salary_from

        avg_salary = (start_salary + end_salary) // 2
        return value_from <= avg_salary <= value_to

    def formatting_vacancy(self):
        vacancy_fields = {
            "vacancy_id": self.vacancy_id,
            "vacancy_name": self.vacancy_name,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "vacancy_url": self.vacancy_url,
            "city": self.city,
            "experience": self.experience,
            "employer": self.employer,
            "platform": self.__platform,
        }
        return vacancy_fields

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}({self.vacancy_id}, "
                f"{self.vacancy_name}, {self.salary_from}, "
                f"{self.salary_to}, {self.__city}, "
                f"{self.__experience}, {self.__employer})")

    def __str__(self) -> str:
        return (f"Название вакансии - {self.vacancy_name}\n"
                f"{self.check_salary}\n"
                f"Требуемый опыт {self.experience}\n"
                f"Наименование организации - {self.__employer}\n"
                f"Город расположения - {self.__city}\n"
                f"Ссылка на вакансию - {self.__vacancy_url}\n")

    def __gt__(self, other) -> bool:
        return self.value > other.value
