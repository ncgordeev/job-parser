import requests

from config import headers, HH_BASE_URL
from src.apis.base_class import BaseAPI


class HeadHunterAPI(BaseAPI):

    def __init__(self, city_name: str, key_word: str,
                 experience: int, salary: int) -> None:
        self.city_name = city_name
        self.key_word = key_word
        self.experience = experience
        self.salary = salary

    def get_city_id(self) -> str:
        """
        Get area id for request
        :return: area id
        """
        default_area_id: str = "113"
        params = {
            "text": self.city_name
        }

        response = requests.get(HH_BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            areas_list = response.json()["items"]
            for area in areas_list:
                area_name = area["area"]["name"]
                if self.city_name == area_name:
                    return area["area"]["id"]

            return default_area_id
        else:
            raise requests.HTTPError(f"Возникла ошибка подключения."
                                     f"Статус ответа - {response.status_code}")

    def get_city_name(self):
        if self.get_city_id() == "113":
            return "Россия"
        else:
            return self.city_name

    def get_experience_id(self) -> str:
        """
        Get experience id for requests
        :return:
        """
        experience_list = {
            range(0, 2): "noExperience",
            range(1, 4): "between1And3",
            range(3, 7): "between3And6",
            range(6, 30): "moreThan6",
        }
        default_id = experience_list[range(0, 2)]

        for key in experience_list.keys():
            if self.experience in key:
                return experience_list[key]
        return default_id

    def get_vacancies(self):
        """
        Make a request for getting a JSON-file with vacations
        :return:
        """
        params = {
            "page": 0,
            "per_page": 100,
            "text": self.key_word,
            "search_field": "name",
            "experience": self.get_experience_id(),
            "area": self.get_city_id(),
            "currency": "RUR",
            "salary": self.salary,
        }

        vacancies_list = []

        while True:
            response = requests.get(HH_BASE_URL, headers=headers, params=params)
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
                print(f"Страница {page + 1} из {pages}")
                if page == pages - 1:
                    print(f"Найдено вакансий - {found_item}")
                    return vacancies_list
                params["page"] += 1
            else:
                raise requests.HTTPError(f"Возникла ошибка подключения."
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
