import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Peygard:
    def __init__(
        self,
        app_list_url,
        app_list_file_dir,
        app_details_url,
        app_reviews_url,
        app_achievements_url,
        app_achievements_gp_url,
    ):
        self.app_list_url = app_list_url
        self.app_list_file_dir = app_list_file_dir
        self.app_list = None
        self.app_details_url = app_details_url
        self.app_reviews_url = app_reviews_url
        self.app_achievements_url = app_achievements_url
        self.app_achievements_gp_url = app_achievements_gp_url

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

    def get_app_reviews(
        self,
        app_id,
        filter="recent",
        language="all",
        cursor="*",
        review_type="all",
        purchase_type="steam",
        num_per_page=100,
        filter_offtopic_activity=0,
    ):
        print("requestng", self.app_reviews_url, app_id)
        response = requests.get(
            f"{self.app_reviews_url}{app_id}",
            params={
                "json": 1,
                "filter": filter,
                "language": language,
                "cursor": cursor,
                "review_type": review_type,
                "purchase_type": purchase_type,
                "num_per_page": num_per_page,
                "filter_offtopic_activity": filter_offtopic_activity,
            },
        )

        with open(os.path.join("data", f"{app_id}-reviews.json"), "w") as app:
            data = response.json()
            json.dump(data, app)

        return response

    def get_app_achievements_info(self, app_id, language="english", format="json"):
        response = requests.get(
            self.app_achievements_url,
            params={
                "appid": app_id,
                "key": os.environ["STEAM_API_KEY"],
                "l": language,
                "format": format,
            },
        )
        with open(os.path.join("data", f"{app_id}-achievements.json"), "w") as app:
            data = response.json()
            json.dump(data, app)

        response = requests.get(
            self.app_achievements_gp_url,
            params={
                "gameid": app_id,
                "format": format,
            },
        )
        with open(
            os.path.join("data", f"{app_id}-achievements-global-percentage.json"), "w"
        ) as app:
            data = response.json()
            json.dump(data, app)
