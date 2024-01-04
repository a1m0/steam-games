import requests
import json
import os
from bs4 import BeautifulSoup
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
        app_players_history_url,
    ):
        self.app_list_url = app_list_url
        self.app_list_file_dir = app_list_file_dir
        self.app_list = None
        self.app_details_url = app_details_url
        self.app_reviews_url = app_reviews_url
        self.app_achievements_url = app_achievements_url
        self.app_achievements_gp_url = app_achievements_gp_url
        self.app_players_history_url = app_players_history_url

    def get_app_list(self):
        source = "Unknown"
        if os.path.isfile(self.app_list_file_dir) is True:
            source = "Local File"
            with open(self.app_list_file_dir, "r") as f:
                self.app_list = json.load(f)
        else:
            source = "Steam API"
            response = requests.get(self.app_list_url)

            with open(self.app_list_file_dir, "w") as app_list_file:
                data = response.json()
                self.app_list = data
                json.dump(data, app_list_file)

        print(
            f"{len(self.app_list['applist']['apps'])} games fetched successfully from {source}!!!"
        )
        return self.app_list

    def get_app_details(self, app_id, currency="us", language="en"):
        response = requests.get(
            self.app_details_url,
            params={"appids": app_id, "cc": currency, "l": language},
        )

        if not os.path.exists(os.path.join("data", str(app_id))):
            os.makedirs(os.path.join("data", str(app_id)))

        with open(os.path.join("data", str(app_id), "details.json"), "w") as d:
            data = response.json()
            json.dump(data, d)

        print(f"Successfully created {app_id} details file.")
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

        if not os.path.exists(os.path.join("data", str(app_id))):
            os.makedirs(os.path.join("data", str(app_id)))

        with open(os.path.join("data", str(app_id), "reviews.json"), "w") as r:
            data = response.json()
            json.dump(data, r)

        print(f"Successfully created {app_id} reviews file.")
        return response

    def get_app_achievements_info(self, app_id, language="english", format="json"):
        if not os.path.exists(os.path.join("data", str(app_id))):
            os.makedirs(os.path.join("data", str(app_id)))

        response = requests.get(
            self.app_achievements_url,
            params={
                "appid": app_id,
                "key": os.environ["STEAM_API_KEY"],
                "l": language,
                "format": format,
            },
        )
        with open(os.path.join("data", str(app_id), "achievements.json"), "w") as a:
            data = response.json()
            json.dump(data, a)
        print(f"Successfully created {app_id} achievements file.")

        response = requests.get(
            self.app_achievements_gp_url,
            params={
                "gameid": app_id,
                "format": format,
            },
        )
        with open(
            os.path.join("data", str(app_id), "achievements-global-percentage.json"),
            "w",
        ) as agp:
            data = response.json()
            json.dump(data, agp)
        print(f"Successfully created {app_id} achievements-global-percentage file.")

    def get_app_players_history(self, app_id):
        page = requests.get(self.app_players_history_url + f"{app_id}")
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find(class_="common-table")
        table_rows = None
        if table:
            table_rows = table.find("tbody").find_all("tr")
        else:
            print(f"app with app id: {app_id} does not have any players history.")
            return None

        history = []
        for row in table_rows:
            cleaned_data = {
                "month": row.find(class_="month-cell").text.strip(),
                "avg_players": row.find(class_="num-f").text,
                "gain_number": row.find(class_="num-p").text,
                "gain_percent": row.find_all("td")[-2].text.replace("%", ""),
                "peak_players": row.find_all("td")[-1].text,
            }
            history.append(cleaned_data)

        if not os.path.exists(os.path.join("data", str(app_id))):
            os.makedirs(os.path.join("data", str(app_id)))

        with open(os.path.join("data", str(app_id), "players-history.json"), "w") as ph:
            data = {"history": history}
            json.dump(data, ph)

        print(f"Successfully created {app_id} players-history file.")
        return history
