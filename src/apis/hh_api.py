import requests

from config import headers, HH_BASE_URL
from base_class import BaseAPI


class HeadHunterAPI(BaseAPI):

    def __init__(self, city_name: str, key_word: str,
                 experience: int, salary: int) -> None:
        self.city_name = city_name
        self.key_word = key_word
        self.experience = experience
        self.salary = salary

    def get_city_id(self) -> str:

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

    def get_experience_id(self) -> str:

        experience_list = {
            range(0, 2): "noExperience",
            range(1, 4): "between1And3",
            range(3, 7): "between3And6",
            range(6, 30): "moreThan6",
        }
        default_id = experience_list[range(0, 2)]

        for key in experience_list.keys():
            print(key)
            if self.experience in key:
                return experience_list[key]
        return default_id

    def get_vacancies(self):

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

        response = requests.get(HH_BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            raw_json = response.json()
            return raw_json
        else:
            raise requests.HTTPError(f"Возникла ошибка подключения."
                                     f"Статус ответа - {response.status_code}")

    def __repr__(self):
        return (f"{__class__.__name__}({self.city_name}, "
                f"{self.key_word}, {self.experience}, {self.salary})")

    def __str__(self):
        return (f"{__class__.__name__}:\n"
                f"Город - {self.city_name},\n"
                f"Ключевой запрос - {self.key_word}\n"
                f"Зарплата - {self.salary}"
                )
