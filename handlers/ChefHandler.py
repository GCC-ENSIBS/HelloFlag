from tornado.options import options

from handlers.BaseHandlers import BaseHandler
from libs.SecurityDecorators import authenticated


class ChefHandler(BaseHandler):
    @authenticated
    def get(self):
        if not options.use_cyberchef:
            self.redirect("/404")
            return
        with open("cyberchef/CyberChef.html", "r") as myfile:
            data = myfile.read()
        self.write(data)
