from utils.user_interaction import user_interaction, get_sorted_obj
from src.savers.json_saver import JSONSaver

if __name__ == "__main__":
    ui = user_interaction()
    js = JSONSaver()
    vacancies_list = get_sorted_obj(ui)

    for vacancy in vacancies_list:
        js.save_data(vacancy.formatting_vacancy())

    index = 1
    for vacancy in vacancies_list:
        print(f"{index} - {vacancy}")
        index += 1
