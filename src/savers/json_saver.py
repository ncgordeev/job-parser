import json
import os

from config import DATA_FOLDER, DATA_FILE
from src.savers.base_saver import BaseSaver
from src.vacancies.vacancy_processor import VacancyProcessor


class JSONSaver(BaseSaver):

    @staticmethod
    def save_data(data):
        if os.path.exists(DATA_FOLDER):
            with open(DATA_FILE, "a", encoding="utf-8") as file:
                if os.stat(DATA_FILE).st_size == 0:
                    json.dump([data], file, indent=2, ensure_ascii=False)
                else:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        reading_data = json.load(f)
                    reading_data.append(data)
                    with open(DATA_FILE, "w", encoding="utf-8") as fr:
                        json.dump(reading_data, fr, indent=2, ensure_ascii=False)
        else:
            os.mkdir(DATA_FOLDER)

    def get_data(self, file_path):
        pass

    @staticmethod
    def get_vacancy_by_salary(value: str):
        value_from, value_to = list(map(int, value.split("-")))
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
            if len(in_range_vacancies) == 0:
                print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос.\n")

            return in_range_vacancies
