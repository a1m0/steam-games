from peygard import Peygard

print("who")
p = Peygard(
    app_list_url="https://api.steampowered.com/ISteamApps/GetAppList/v0002/",
    app_list_file_dir="data/app_list.json",
    app_details_url="https://store.steampowered.com/api/appdetails/",
    app_reviews_url="https://store.steampowered.com/appreviews/",
    app_achievements_url="https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v0002/",
    app_achievements_gp_url="https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/",
)
# p.get_app_list()
# print(p.app_list)
# print(p.get_app_reviews(app_id=1086940, language="english").json())
p.get_app_achievements_info(app_id=1086940)
