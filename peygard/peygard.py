import requests
import json
import os


class Peygard:
    def __init__(self, app_list_url, app_list_file_dir, app_details_url):
        self.app_list_url = app_list_url
        self.app_list_file_dir = app_list_file_dir
        self.app_list = None
        self.app_details_url = app_details_url

    def get_app_list(self):
        if self.app_list_file_dir is not None:
            with open(self.app_list_file_dir, "r") as f:
                self.app_list = json.load(f)
        else:
            response = requests.get(self.app_list_url)

            with open(self.app_list_file_dir, "w") as app_list_file:
                data = response.json()
                self.app_list = data
                json.dump(data, app_list_file)

            return response

    def get_app_details(self, app_id, currency="us", language="en"):
        response = requests.get(
            self.app_details_url,
            params={"appids": app_id, "cc": currency, "l": language},
        )

        with open(os.path.join("data", f"{app_id}.json"), "w") as app:
            data = response.json()
            json.dump(data, app)

        return response
