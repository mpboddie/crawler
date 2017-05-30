import json

class SearchItems:

    with open('config.json', 'r') as json_data:
        site = json.load(json_data)["siteSettings"]["address"]

class Show(SearchItems):

    def __init__(self, title, season, vidFormat, resolution, site=None):
        self.title = title
        self.season = season

        if (isinstance(vidFormat, list)):
            self.vidFormat = vidFormat
        else:
            self.vidFormat = [vidFormat]

        if (isinstance(resolution, list)):
            self.resolution = resolution
        else:
            self.resolution = [resolution]

        if site is not None:
            self.site = site

    def searchSite(self):
        return "Searching {} for an episode of {} from season {}.".format(self.site, self.title, self.season)
