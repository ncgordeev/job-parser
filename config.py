import os
from fake_useragent import UserAgent

ua = UserAgent()
ua_random = ua.random

headers = {
    "User-Agent": ua_random,
}

AREAS_URL = "https://api.hh.ru/areas/"
HH_BASE_URL = "https://api.hh.ru/vacancies"
SJ_API_URL = "https://api.superjob.ru/2.0/vacancies/"

ROOT_PATH = os.path.dirname(__file__)
DATA_FOLDER = os.path.join(ROOT_PATH, "data")
DATA_FILE = os.path.join(ROOT_PATH, DATA_FOLDER, "all_vacancies.json")

SJ_API_KEY = os.environ.get("SJ_API_KEY")
