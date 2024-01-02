import requests
import json


class Peygard:
    def __init__(self, app_list_url, app_list_file_dir):
        self.app_list_url = app_list_url
        self.app_list_file_dir = app_list_file_dir
        self.app_list = None

    def get_app_list(self):
        response = requests.get(self.app_list_url)

        with open(self.app_list_file_dir, "w") as app_list_file:
            data = response.json()
            self.app_list = data
            json.dump(data, app_list_file)

        return response
