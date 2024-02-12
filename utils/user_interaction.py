import os
import time

from config import DATA_FILE

from src.apis.hh_api import HeadHunterAPI
from src.apis.sj_apy import SuperJobAPI
from src.vacancies.vacancy_processor import VacancyProcessor
from src.savers.json_saver import JSONSaver


def user_interaction():
    js = JSONSaver()
    index = 1
    print(
        "Добро пожаловать! С помощью данной программы Вы можете осуществить подбор вакансии своей мечты!\n"
    )
    time.sleep(0.2)

    while True:
        user_choice_start = input(
            "Для начала работы с программой введите цифру 1.\n"
            "Введите 0, если хотите выйти. ").strip()

        if user_choice_start not in ("0", "1"):
            print("Вы ввели некорректные данные. Попробуйте снова.\n")

        elif user_choice_start == "0":
            break

        elif user_choice_start == "1":

            user_make_request = input(
                "Если Вы хотите создать запрос - впишите 1. \n"
                "Для работы с существующим файлом - 2 ").strip()

            if user_make_request not in ("1", "2"):
                print("Неверный выбор. Попробуйте снова")
                continue

            elif user_make_request == "1":

                user_choice_platform = input(
                    "Выберите платформу для поиска: \n"
                    "1 - 'HeadHunter'\n"
                    "2 - 'Super Job'\n").strip()

                user_city_query = input(
                    "Введите название города, в котором планируете искать работу.\n"
                    "Иначе нажмите Enter (поиск будет осуществлен по всем регионам РФ): "
                ).lower().strip()

                user_keyword_query = input(
                    "Введите ключевую фразу для поиска. Например Python-разработчик: "
                ).lower().strip()

                user_experience_query = input("Выберите релевантный опыт:\n"
                                              "1 - Менее года\n"
                                              "2 - От года до 3\n"
                                              "3 - От 3 до 6 лет\n"
                                              "4 - Свыше 6 лет: ")

                if user_experience_query in ("1", "2", "3", "4",):
                    user_experience_query = int(user_experience_query)
                elif user_experience_query == "":
                    user_experience_query = None

                else:
                    print("Вы ввели некорректные данные для выбора опыта. Введите число.\n")
                    continue

                user_salary_query = input("Укажите интересующую зарплату: \n").strip()

                if user_salary_query.isdigit():
                    user_salary_query = int(user_salary_query)
                elif user_salary_query in ("", 0):
                    user_salary_query = 0
                else:
                    print("Вы ввели некорректные данные по зарплате. Введите число.\n")
                    continue

                if user_choice_platform == "1":
                    hh_query = HeadHunterAPI(
                        user_city_query,
                        user_keyword_query,
                        user_experience_query,
                        user_salary_query
                    )
                    return hh_query

                elif user_choice_platform == "2":
                    sj_query = SuperJobAPI(
                        user_city_query,
                        user_keyword_query,
                        user_experience_query,
                        user_salary_query
                    )
                    return sj_query

            elif user_make_request == "2":

                if os.path.exists(DATA_FILE):
                    user_sort_method = input(
                        "\nВыберите действие: \n"
                        "1 - Вывести топ вакансий по зарплате \n"
                        "2 - Вывести вакансии, которые входят в  диапазон зарплат \n"
                        "3 - Вывести вакансии по названию \n"
                    )

                    if user_sort_method not in ("1", "2", "3"):
                        print("Введено неизвестное значение. Попробуйте еще раз.\n")

                    elif user_sort_method == "1":
                        number = input("Введите количество вакансий(по умолчанию - 10) \n").strip()
                        if not isinstance(number, int):
                            number = 10
                        else:
                            number = int(number)
                        top_vacancies = js.get_top_vacancies(number)

                        for vacancy in top_vacancies:
                            print(f"{index} - {vacancy}")
                            index += 1

                    elif user_sort_method == "2":
                        in_range_number = input(
                            "Введите диапазон зарплат.\n"
                            "Например: 50000-100000 ").strip()
                        value_from, value_to = list(
                            map(int, in_range_number.split("-")))

                        in_range_vacancies = js.get_vacancy_by_salary(value_from, value_to)

                        if not in_range_vacancies:
                            print(
                                "\nПодходящих вакансий не найдено. Попробуйте изменить запрос.\n"
                            )
                            exit()

                        for range_vacancy in in_range_vacancies:
                            print(f"{index} - {range_vacancy}")
                            index += 1

                    elif user_sort_method == "3":
                        vacancy_title = input("\nВведите ключевое слово "
                                              "для поиска вакансий по названию: \n").strip()
                        vacancies_by_title = js.get_vacancy_by_title(vacancy_title)

                        if not vacancies_by_title:
                            print(
                                "\nПодходящих вакансий не найдено. Попробуйте изменить запрос.\n"
                            )
                            exit()

                        for vacancy_by_title in vacancies_by_title:
                            print(f"{index} - {vacancy_by_title}")
                            index += 1
                else:
                    print(
                        "Файл не найден. Сначала необходимо сформировать запрос. \n"
                    )
                    continue
        else:
            print("Введено неизвестное значение. Попробуйте еще раз.\n")
            continue


def get_sorted_obj(user_data):
    vacancies_list = user_data.get_vacancies()
    vacancies_obj = []

    for vacancy in vacancies_list:
        vp = VacancyProcessor(**vacancy)
        vacancies_obj.append(vp)

    sorted_obj = sorted(vacancies_obj, reverse=True)
    return sorted_obj
