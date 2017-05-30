import json
import searchItems

with open('config.json', 'r') as json_data:
    config = json.load(json_data)

#print(config["siteSettings"]["address"])

with open('search.json', 'r') as json_data:
    search = json.load(json_data)

#print(search[0]["title"])

for show in search:
    tvshow = searchItems.Show(show["title"], show["season"], show["format"], show["resolution"])
    print(tvshow.searchSite())
