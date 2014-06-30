import sys
import mechanize
import re

# URI of ZNC server webdmin access
URI = "https://107.170.134.161:5001/"

class ZNCServer():

    def __init__(self):
        # Create a mechanize Browser ob
        self.br = mechanize.Browser(factory=mechanize.RobustFactory())

        # Ignore the robots.txt file
        self.br.set_handle_robots(False)

        # Login to the webadmin
        self.br.open(URI)
        self.br.select_form(nr=0)
        self.br.form['user'] = 'znc-admin'
        self.br.form['pass'] = 'password'
        self.br.submit()

    @property
    def users(self):
        self.br.follow_link(text="List Users")
        users = []
        for link in self.br.links():
            if link.url.startswith("adduser?clone="):
                users.append(link.url[14:])
        return users

    def add_user(self, username, password):
        self.br.follow_link(text="List Users")
        resp = self.br.follow_link(url="adduser?clone=userbase")
        resp.set_data(self.br.response().read().replace('datalist', 'select'))
        self.br.set_response(resp)
        self.br.select_form(nr=0)
        self.br.form['user'] = self.br.form['nick'] = self.br.form['altnick'] = self.br.form['ident'] = self.br.form['realname'] = username
        self.br.form['password'] = self.br.form['password2'] = password
        self.br.submit()


