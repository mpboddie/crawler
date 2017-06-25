import json
import re
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

    season = None
    episode = None


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

        self.browser.get(self.site + 't')

        if check_exists_by_id(self.browser, "login"):
            if not self.login():
                return "ERROR: Problem logging in"

        print(check_exists_by_id(self.browser, "iptStart"))
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
                    self.season = None
                    self.episode = None
                    if self.parseTitle(row.find_element_by_class_name('b').text):
                        print("Download: " + row.find_element_by_xpath('.//td[4]/a').get_attribute('href'))
                    else:
                        continue

    def parseTitle(self, fullTitle):
        if bool(re.match(self.title, fullTitle, re.I)):
            # The unparsed string starts with the correct title
            p = re.compile("[Ss](\d{2})[Ee](\d{2})")        # find the pattern of S##E##, case-insensitive and capture the digits
            m = p.search(fullTitle)
            if m:
                self.season = m.group(1)
                self.episode = m.group(2)
                print("Found season {} episode {} of {}".format(self.season, self.episode, self.title))
                return True
            else:
                return False
        else:
            return False
