from src.vacancies.vacancy_processor import VacancyProcessor
from utils.user_interaction import user_interaction
from src.savers.json_saver import JSONSaver

if __name__ == "__main__":
    hh = user_interaction()
    js = JSONSaver()
    vacancies_list = hh.get_vacancies()
    vacancies_obj = []

    for vacancy in vacancies_list:
        vp = VacancyProcessor(**vacancy)
        vacancies_obj.append(vp)

    sorted_obj = sorted(vacancies_obj)

    for obj in sorted_obj:
        js.save_data(obj.formatting_vacancy())
