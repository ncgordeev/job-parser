import time
from src.apis.hh_api import HeadHunterAPI
from src.apis.sj_apy import SuperJobAPI
from src.vacancies.vacancy_processor import VacancyProcessor


def user_interaction():
    print("Добро пожаловать! С помощью данной программы Вы можете осуществить подбор вакансии своей мечты!\n")
    time.sleep(0.2)

    while True:
        user_choice = input("Для начала работы с программой введите цифру 1.\n"
                            "Введите 0, если хотите выйти. ")

        if user_choice not in ("0", "1"):
            print("Вы ввели некорректные данные. Попробуйте снова.\n")
        elif user_choice == "0":
            break
        elif user_choice == "1":
            user_choice_platform = input("Выберите платформу для поиска: \n"
                                         "1 - 'HeadHunter'\n"
                                         "2 - 'Super Job'\n")
            user_city_query = input(
                "Введите название города, в котором планируете искать работу.\n"
                "Иначе нажмите Enter (поиск будет осуществлен по всем регионам РФ): ").lower().strip()
            user_keyword_query = input(
                "Введите ключевую фразу для поиска. Например Python-разработчик: ").lower().strip()
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

            user_salary_query = input("Укажите интересующую зарплату: ")
            if user_salary_query.isdigit():
                user_salary_query = int(user_salary_query)
            elif user_salary_query in ("", 0):
                user_salary_query = 0
            else:
                print("Вы ввели некорректные данные по зарплате. Введите число.\n")
                continue

            if user_choice_platform == "1":
                hh_query = HeadHunterAPI(user_city_query, user_keyword_query,
                                         user_experience_query, user_salary_query)
                return hh_query

            elif user_choice_platform == "2":
                sj_query = SuperJobAPI(user_city_query, user_keyword_query,
                                       user_experience_query, user_salary_query)
                return sj_query

        else:
            print("Введено неизвестное значение. Попробуйте еще раз.\n")


def get_sorted_obj(user_data):
    vacancies_list = user_data.get_vacancies()
    vacancies_obj = []

    for vacancy in vacancies_list:
        vp = VacancyProcessor(**vacancy)
        vacancies_obj.append(vp)

    sorted_obj = sorted(vacancies_obj)
    return sorted_obj
