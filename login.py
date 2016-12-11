import tornado.httpserver
import tornado.ioloop
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
    	username = self.get_argument("username")
    	password = self.get_argument("password")
    	if self.check_identity(username, password):
        	self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/modify")

    def check_identity(self, username, password):
    	if username == "admin" and password == "password":
    		return True
    	return False

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
        	self.clear_cookie("username")
        	self.redirect("/login")