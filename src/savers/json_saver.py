import json
import os

from config import DATA_FOLDER, DATA_FILE
from src.savers.base_saver import BaseSaver
from src.vacancies.vacancy_processor import VacancyProcessor


class JSONSaver(BaseSaver):

    @staticmethod
    def save_data(data):
        if not os.path.exists(DATA_FOLDER):
            os.mkdir(DATA_FOLDER)
        with open(DATA_FILE, "a", encoding="utf-8") as file:
            if os.stat(DATA_FILE).st_size == 0:
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
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                vacancies = json.load(file)
            list_vacancy = [VacancyProcessor(**item) for item in vacancies]

            if len(list_vacancy) <= number:
                return list_vacancy
            else:
                return list_vacancy[:number]
        else:
            return None

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

        vacancies_by_title = []
        for vacancy in list_vacancy:
            if key_word.lower() in vacancy.vacancy_name.lower():
                vacancies_by_title.append(vacancy)

        return vacancies_by_title

    @staticmethod
    def get_vacancy_by_salary(value_from: int, value_to: int):
        """
        Method get list of vacancies by salary
        :param value_from:
        :param value_to:
        :return:
        """
        in_range_vacancies = []

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
            list_vacancy = [VacancyProcessor(**item) for item in vacancies]

        for vacancy in list_vacancy:
            start_salary = vacancy.salary_from
            end_salary = vacancy.salary_to

            if not isinstance(start_salary, int) and isinstance(end_salary, int):
                start_salary = end_salary
            elif isinstance(start_salary, int) and not isinstance(end_salary, int):
                end_salary = start_salary

            avg = (start_salary + end_salary) // 2
            if value_from <= avg <= value_to:
                in_range_vacancies.append(vacancy)

        return in_range_vacancies
