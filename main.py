'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import logging
from controllers import person, server
from config import config
import webapp2


# must fix list prio
app = webapp2.WSGIApplication([
        # Essential handlers
        ("/AJAX/person/get/current", person.GetCurrentPersonHanlder),
        ("/login/", person.RegisterPersonHandler),
        ("/register/", person.RegisterPersonHandler),
        ("/logout/", person.LogoutPersonHandler),
        ('/', server.RootPage),
    ],debug=True, config=config.config)


# Extra Hanlder like 404 500 etc
def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! Naughty Mr. Jiggles (This is a 404)')
    response.set_status(404)

app.error_handlers[404] = handle_404
