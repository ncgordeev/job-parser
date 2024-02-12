import requests
import time

from config import headers, HH_BASE_URL, AREAS_URL
from src.apis.base_class import BaseAPI


class HeadHunterAPI(BaseAPI):

    def __init__(self, city_name: str, key_word: str,
                 experience: int, salary: int) -> None:
        self.city_name = city_name
        self.key_word = key_word
        self.experience = experience
        self.salary = salary
        self.params = {
            "page": 0,
            "per_page": 100,
            "text": self.key_word,
            "experience": "noExperience",
            "area": self.get_city_id(),
            "currency": "RUR",
            "salary": self.salary,
        }
        self.get_experience_id()
        self.get_salary_query()

    def get_city_id(self) -> str:
        """
        Get area id for request
        :return: area id
        """
        default_area_id: str = "113"
        params = {
            "text": self.city_name
        }

        response = requests.get(AREAS_URL, headers=headers, params=params)
        if response.status_code == 200:
            areas_list = response.json()[0]["areas"]
            for area in areas_list:
                if area["name"].lower() == self.city_name.lower():
                    return area["id"]
                area_dippers = area["areas"]
                for area_dipper in area_dippers:
                    if area_dipper["name"].lower() == self.city_name.lower():
                        return area_dipper["id"]
            return default_area_id
        else:
            raise requests.HTTPError(f"Возникла ошибка подключения."
                                     f"Статус ответа - {response.status_code}")

    def get_city_name(self):
        if self.get_city_id() == "113":
            return "Россия"
        else:
            return self.city_name

    def get_experience_id(self) -> None:
        """
        Get experience id for requests
        :return:
        """
        experience_list = {
            1: "noExperience",
            2: "between1And3",
            3: "between3And6",
            4: "moreThan6",
        }
        if self.experience is None:
            del self.params["experience"]
        else:
            for key in experience_list.keys():
                if self.experience == key:
                    self.params["experience"] = experience_list[key]

    def get_salary_query(self):
        if not self.salary:
            del self.params["salary"]

    def get_vacancies(self) -> list:
        """
        Make a request for getting a JSON-file with vacations
        :return:
        """

        vacancies_list = []

        while True:
            response = requests.get(HH_BASE_URL, headers=headers, params=self.params)
            if response.status_code == 200:
                raw_json = response.json()
                page = raw_json["page"]
                pages = raw_json["pages"]
                items = raw_json["items"]
                found_item = raw_json["found"]
                for item in items:
                    if item["salary"]:
                        s_from = item.get("salary").get("from")
                        s_to = item.get("salary").get("to")
                        valid_currency = item.get("salary").get("currency")
                        if valid_currency != "RUR":
                            continue
                    else:
                        s_from = s_to = 0

                    data = {
                        "vacancy_id": item["id"],
                        "vacancy_name": item["name"],
                        "salary_from": s_from,
                        "salary_to": s_to,
                        "vacancy_url": item["alternate_url"],
                        "city": item["area"]["name"],
                        "experience": item["experience"]["name"],
                        "employer": item["employer"]["name"],
                        "platform": "headhunter",
                    }
                    vacancies_list.append(data)
                    time.sleep(0.1)
                print(f"Страница {page + 1} из {pages} \n")
                if page == pages - 1:
                    print(f"Найдено вакансий - {found_item} \n")
                    return vacancies_list
                self.params["page"] += 1
            else:
                raise requests.HTTPError(f"Возникла ошибка подключения. "
                                         f"Статус ответа - {response.status_code}")

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.city_name}, "
                f"{self.key_word}, {self.experience}, {self.salary})")

    def __str__(self):
        return (f"{self.__class__.__name__}:\n"
                f"Регион поиска - {self.get_city_name()},\n"
                f"Ключевой запрос - {self.key_word}\n"
                f"Зарплата - {self.salary}"
                )
