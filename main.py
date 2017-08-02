import json
import searchItems
import boxServer

with open('search.json', 'r') as json_data:
    search = json.load(json_data)

box = boxServer.BoxServer()

for show in search:
    tvshow = searchItems.Show(show["title"], show["season"], show["format"], show["resolution"], box)
    tvshow.searchSite()

#box.quit()
