import mechanize

# URI of ZNC server webdmin access
URI = "https://107.170.134.161:5001/"

class ZNCServer():

    def __init__(self, admin_password, uri=URI):
        """ Initialize a mechanize Browser object and login as an admin """

        # Create a mechanize Browser ob
        self.br = mechanize.Browser(factory=mechanize.RobustFactory())

        # Ignore the robots.txt file
        self.br.set_handle_robots(False)

        # Login to the webadmin
        self.br.open(uri)
        self.br.select_form(nr=0)
        self.br.form['user'] = 'znc-admin'
        self.br.form['pass'] = admin_password
        self.br.submit()

    @property
    def users(self):
        """
        :return: list of users
        """
        self.br.follow_link(text="List Users")

        return [link.url[14:] for link in self.br.links()
                if link.url.startswith("adduser?clone=")]

    def add_user(self, username, password):
        """ Add a user """
        
        self.br.follow_link(text="List Users")

        # Clean HTML
        resp = self.br.follow_link(url="adduser?clone=userbase")
        resp.set_data(self.br.response().read().replace('datalist', 'select'))
        self.br.set_response(resp)

        # Fill in the form
        self.br.select_form(nr=0)
        self.br.form['user'] = self.br.form['nick'] = self.br.form['altnick'] = self.br.form['ident'] = self.br.form['realname'] = username
        self.br.form['password'] = self.br.form['password2'] = password
        self.br.submit()


