from peygard import Peygard
import time

p = Peygard(
    app_list_url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/",
    app_list_file_dir="data/app_list.json",
    app_details_url="https://store.steampowered.com/api/appdetails/",
    app_reviews_url="https://store.steampowered.com/appreviews/",
    app_achievements_url="https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002/",
    app_achievements_gp_url="https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/",
    app_players_history_url="https://steamcharts.com/app/",
)

p.get_app_list()

for app in p.app_list["applist"]["apps"][:10]:
    print(app)
    p.get_app_details(app_id=app["appid"])
    p.get_app_reviews(app_id=app["appid"])
    p.get_app_achievements_info(app_id=app["appid"])
    p.get_app_players_history(app_id=app["appid"])

    time.sleep(5)
