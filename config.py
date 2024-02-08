import os
from fake_useragent import UserAgent

ua = UserAgent()
ua_random = ua.random

headers = {
    "User-Agent": ua_random,
}

HH_BASE_URL = "https://api.hh.ru/vacancies"

ROOT_PATH = os.path.dirname(__file__)
DATA_FILE = os.path.join(ROOT_PATH, "data", "all_vacancies.json")
