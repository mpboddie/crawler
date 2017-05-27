import json

with open('config.json', 'r') as json_data:
    config = json.load(json_data)

print(config["siteSettings"]["address"])

with open('search.json', 'r') as json_data:
    search = json.load(json_data)

print(search[0]["title"])
