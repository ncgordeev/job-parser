from abc import ABC, abstractmethod


class BaseSaver(ABC):

    @staticmethod
    def save_data(data):
        pass

    @abstractmethod
    def get_top_vacancies(self, number):
        pass

    @staticmethod
    def get_vacancy_by_title(key_word):
        pass
