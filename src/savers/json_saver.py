import json
import os

from config import DATA_FOLDER, DATA_FILE
from src.savers.base_saver import BaseSaver
from src.vacancies.vacancy_processor import VacancyProcessor


class JSONSaver(BaseSaver):

    @staticmethod
    def save_data(data):
        """
        This method saving the data after request
        :param data:
        :return:
        """
        if not os.path.exists(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)
        mode = 'a' if os.path.exists(DATA_FILE) else 'w'
        with open(DATA_FILE, mode, encoding="utf-8") as file:
            if mode == 'w':
                json.dump([data], file, indent=2, ensure_ascii=False)
            else:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    reading_data = json.load(f)
                reading_data.append(data)
                with open(DATA_FILE, "w", encoding="utf-8") as fr:
                    json.dump(reading_data, fr, indent=2, ensure_ascii=False)

    def get_top_vacancies(self, number: int):
        """
        Get list of top vacancies
        :param number:
        :return:
        """
        if not os.path.exists(DATA_FILE):
            return None

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            vacancies = json.load(file)

        list_vacancy = [VacancyProcessor(**item) for item in vacancies]

        top_vacancies = [vacancy for vacancy in list_vacancy if vacancy.has_salary()]

        return top_vacancies[0:number] if len(top_vacancies) > number else top_vacancies

    @staticmethod
    def get_vacancy_by_title(key_word: str):
        """
        Method get list of vacancies by title
        :param key_word:
        :return:
        """
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            vacancies = json.load(file)

        list_vacancy = [VacancyProcessor(**item) for item in vacancies]

        return [vacancy for vacancy in list_vacancy if key_word.lower() in vacancy.vacancy_name.lower()]

    @staticmethod
    def get_vacancy_by_salary(value_from: int, value_to: int):
        """
        Method get list of vacancies by salary
        :param value_from:
        :param value_to:
        :return:
        """
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            vacancies = json.load(file)

        list_vacancy = [VacancyProcessor(**item) for item in vacancies]

        return [
            vacancy for vacancy in list_vacancy
            if vacancy.is_salary_in_range(value_from, value_to)
        ]
