import json
import searchItems

with open('search.json', 'r') as json_data:
    search = json.load(json_data)

for show in search:
    tvshow = searchItems.Show(show["title"], show["season"], show["format"], show["resolution"])
    tvshow.searchSite()
