import json
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

        if check_exists_by_id(self.browser, "login"):
            if not self.login():
                return "ERROR: Problem logging in"

        #login = self.browser.find_element_by_id('login')
        #print(self.browser.page_source)
        self.browser.save_screenshot('screenie.png')
        #self.browser.quit()
        return "Searching {} for an episode of {} from season {}.".format(self.site, self.title, self.season)
