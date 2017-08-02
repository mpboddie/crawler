import json
import ftplib
import searchItems
import string
import re

class BoxServer:

    def __init__(self):
        with open('config.json', 'r') as json_data:
            config = json.load(json_data)

        boxAddress = config["serverSettings"]["address"]
        username = config["serverSettings"]["username"]
        password = config["serverSettings"]["password"]
        location = config["serverSettings"]["location"]

        self.ftp = ftplib.FTP_TLS(boxAddress, username, password)
        self.ftp.prot_p()

    def checkFor(self, title, season, episode, directory):
        files = []
        try:
            files = list(self.ftp.mlsd(directory, []))
        except (ftplib.error_perm, resp):
            print("ERROR: " + str(resp))
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise

        translator = re.compile('[%s]' % re.escape(string.punctuation))

        for filename in files:
            lessPunct = re.sub('[%s]' % re.escape(string.punctuation), ' ', filename[0])
            if title.lower() in lessPunct.lower():  # This file has the title we are checking for
                if ("s"+season+"e"+episode) in lessPunct.lower():   # This file has the season and episode number we are checking for
                    return True     # returning True as we found the item in question

        return False    # No item matched the description

    def quit(self):
        self.ftp.quit()
