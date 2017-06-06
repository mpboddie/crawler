import json
import searchItems

with open('config.json', 'r') as json_data:
    config = json.load(json_data)

with open('search.json', 'r') as json_data:
    search = json.load(json_data)

for show in search:
    tvshow = searchItems.Show(show["title"], show["season"], show["format"], show["resolution"])
    print(tvshow.searchSite())
