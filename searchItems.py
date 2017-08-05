import json
import re
import os
import boxServer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_id(browser,id):
    try:
        browser.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

class SearchItems:

    with open('config.json', 'r') as json_data:
        config = json.load(json_data)

    site = config["siteSettings"]["address"]
    username = config["siteSettings"]["username"]
    password = config["siteSettings"]["password"]

    localPath = config["localSettings"]["rootPath"]
    tvFolder = config["localSettings"]["tvFolder"]

    browser = webdriver.PhantomJS()
    browser.get(site)

    def login(self):
        print("Logging in!")
        try:
            userField = self.browser.find_element_by_name("username")
            passField = self.browser.find_element_by_name("password")
            submit = self.browser.find_element_by_class_name("button")
        except NoSuchElementException:
            return False
        userField.clear()
        userField.send_keys(self.username)
        passField.clear()
        passField.send_keys(self.password)
        submit.click()

        return check_exists_by_id(self.browser, "iptStart")

    def quit(self):
        self.browser.quit()
        return True

class Show(SearchItems):

    tvFormat = {'TV/Web-DL': 13, 'TV/x264': 14, 'TV/x265': 15, 'TV/Xvid': 16}
    resFormat = {'720p': 7, '1080p': 8, '2160p': 9}

    title = None
    season = None
    box = None
    foundSeason = None
    foundEpisode = None


    def __init__(self, title, season, vidFormat, resolution, box, site=None):
        self.title = title
        self.season = season.zfill(2)
        self.box = box

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

        self.browser.get(self.site + 't')

        if check_exists_by_id(self.browser, "login"):
            if not self.login():
                return "ERROR: Problem logging in"

        #print(check_exists_by_id(self.browser, "iptStart"))
        for resPref in self.resolution:
            for vidPref in self.vidFormat:
                # uncheck all catagories
                self.browser.execute_script("$('#catters :input[type=\"checkbox\"]').prop('checked', false);")
                # check the TV format
                self.browser.execute_script('$(\'#catters > table > tbody > tr > td:nth-child(2) > label:nth-child(' + str(self.tvFormat[vidPref]) + ') > input[type="checkbox"]\').prop(\'checked\', true);')
                # check the video resolution
                self.browser.execute_script('$(\'#catters > table > tbody > tr > td:nth-child(6) > label:nth-child(' + str(self.resFormat[resPref]) + ') > input[type="checkbox"]\').prop(\'checked\', true);')
                qInput = self.browser.find_element_by_name('q')
                qInput.clear()
                qInput.send_keys(self.title)
                self.browser.find_element_by_xpath('//*[@id="Search"]/tbody/tr/td/input[2]').click()
                # Get rows
                rows = self.browser.find_elements_by_xpath('//*[@id="torrents"]/tbody/tr[position()>=2]')
                print("Found {} results for episodes of {} in {} format with {} resolution.".format(len(rows), self.title, vidPref, resPref))
                for row in rows:
                    self.foundSeason = None
                    self.foundEpisode = None
                    if self.parseTitle(row.find_element_by_class_name('b').text):
                        if self.season == self.foundSeason:
                            print("Checking for {} S{}E{}".format(self.title, self.foundSeason, self.foundEpisode))
                            if self.checkLocalFor(self.title, self.foundSeason, self.foundEpisode):
                                if not self.box.checkFor(self.title, self.foundSeason, self.foundEpisode, '.'):
                                    if not self.box.checkFor(self.title, self.foundSeason, self.foundEpisode, 'watch'):
                                        print("Download: " + row.find_element_by_xpath('.//td[4]/a').get_attribute('href'))
                                    else:
                                        print("You already have this in watch.")
                                else:
                                    print("You already have this in shows.")
                            else:
                                print("You already have this and it is ready to be viewed.")
                    else:
                        continue

    def parseTitle(self, fullTitle):
        if bool(re.match(self.title, fullTitle, re.I)):
            # The unparsed string starts with the correct title
            p = re.compile("[Ss](\d{2})[Ee](\d{2})")        # find the pattern of S##E##, case-insensitive and capture the digits
            m = p.search(fullTitle)
            if m:
                self.foundSeason = m.group(1).zfill(2)
                self.foundEpisode = m.group(2).zfill(2)
                #print("Found season {} episode {} of {}".format(self.season, self.episode, self.title))
                return True
            else:
                return False
        else:
            return False

    def checkLocalFor(self, title, season, episode):
        showLocation = os.path.join(self.localPath, self.tvFolder, title.lower(), "Season " + season).rstrip()
        print(showLocation + " " + str(os.path.exists(showLocation)))
        if(os.path.exists(showLocation)):
            # a directory exists for the show and season,continue search
            for filename in os.listdir(showLocation):
                if "s"+season+"e"+episode in filename.lower():
                    return True     # the item was found
            return False
        else:
            return False    # the item was not located
