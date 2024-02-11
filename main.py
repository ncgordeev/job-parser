from src.vacancies.vacancy_processor import VacancyProcessor
from utils.user_interaction import user_interaction, get_sorted_obj
from src.savers.json_saver import JSONSaver

if __name__ == "__main__":
    ui = user_interaction()
    vacancies_list = get_sorted_obj(ui)

    for i in vacancies_list:
        print(i)
    js = JSONSaver()

    #
    # for obj in sorted_obj:
    #     js.save_data(obj.formatting_vacancy())
    #
    # number = input("Введите число ")
    # if not isinstance(number, int):
    #     number = 10
    # else:
    #     number = int(number)
    # top_vacancies = js.get_top_vacancies(number)
    #
    # if top_vacancies is None:
    #     user_interaction()
    #     js.get_top_vacancies(number)
    #
    # for i in top_vacancies:
    #     print(i)
    # js = JSONSaver()
    #
    # in_range_vacancies = js.get_vacancy_by_salary("100000-150000")
    #
    # if not in_range_vacancies:
    #     print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос.\n")
    #     exit()
    # for i in in_range_vacancies:
    #     print(i)

    # get_vacancy_by_title = js.get_vacancy_by_title("python")
    # if not get_vacancy_by_title:
    #     print("\nПодходящих вакансий не найдено. Попробуйте изменить запрос.\n")
    #     exit()
    # for i in get_vacancy_by_title:
    #     print(i)
