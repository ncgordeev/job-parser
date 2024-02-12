import requests
import time

from config import SJ_API_URL, SJ_API_KEY, ua_random
from src.apis.base_class import BaseAPI


class SuperJobAPI(BaseAPI):
    headers = {
        "Host": "api.superjob.ru",
        "X-Api-App-Id": SJ_API_KEY,
        "User-Agent": ua_random,
    }

    def __init__(self, city_name: str, key_word: str, experience: int,
                 payment_from: int) -> None:
        self.city_name = city_name
        self.key_word = key_word
        self.experience = experience
        self.payment_from = payment_from

    def get_vacancies(self) -> list:
        """
        Make a request for getting a JSON-file with vacations
        :return:
        """

        params = {
            "id_country": 1,
            "town": self.city_name,
            "keyword": self.key_word,
            "experience": self.experience,
            "payment_from": self.payment_from,
        }

        vacancies_list = []
        page_index = 0

        while True:
            response = requests.get(SJ_API_URL,
                                    headers=self.headers,
                                    params=params)
            if response.status_code == 200:
                raw_json = response.json()
                items = raw_json["objects"]
                page = raw_json["more"]
                vacancies_quantity = raw_json["total"]
                for item in items:
                    salary_from = item.get("payment_from")
                    salary_to = item.get("payment_to")

                    data = {
                        "vacancy_id": item["id"],
                        "vacancy_name": item["profession"],
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "vacancy_url": item["link"],
                        "city": item["town"]["title"],
                        "experience": item["experience"]["title"],
                        "employer": item["firm_name"],
                        "platform": "superjob",
                    }

                    vacancies_list.append(data)
                    time.sleep(0.2)

                page_index += 1
                if len(vacancies_list) != 0:
                    print(
                        f"Всего вакансий {vacancies_quantity}. Страница {page_index}"
                    )
                    return vacancies_list
                else:
                    print(f"Подходящие вакансии не найдены.")
                if page is False:
                    break
            elif response.status_code == 403:
                print("Необходимо авторизоваться при помощи API - ключа")
            else:
                raise requests.HTTPError(
                    f"Возникла ошибка подключения. "
                    f"Статус ответа - {response.status_code}")

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.city_name}, "
                f"{self.key_word}, {self.experience}, {self.payment_from})")

    def __str__(self):
        return (f"{self.__class__.__name__}:\n"
                f"Регион поиска - {self.city_name},\n"
                f"Ключевой запрос - {self.key_word}\n"
                f"Зарплата - от {self.payment_from}")
