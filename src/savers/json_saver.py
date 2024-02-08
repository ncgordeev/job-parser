import json
import os
from config import DATA_FILE
from src.savers.base_saver import BaseSaver


class JSONSaver(BaseSaver):

    @staticmethod
    def save_data(data):
        with open(DATA_FILE, "a", encoding="utf-8") as file:
            if os.stat(DATA_FILE).st_size == 0:
                json.dump([data], file, indent=2, ensure_ascii=False)
            else:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    reading_data = json.load(f)
                reading_data.append(data)
                with open(DATA_FILE, "w", encoding="utf-8") as fr:
                    json.dump(reading_data, fr, indent=2, ensure_ascii=False)

    def get_data(self, file_path):
        pass
