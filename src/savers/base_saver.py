from abc import ABC, abstractmethod


class BaseSaver(ABC):

    @staticmethod
    def save_data(data):
        pass

    @abstractmethod
    def get_data(self, file_path):
        pass
