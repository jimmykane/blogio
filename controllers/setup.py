'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import logging
import webapp2
from models.person import *
from models.jukebox import *
from google.appengine.api import users


class SetupInitHandler(webapp2.RequestHandler):

    def get(self):

        person = Person.get_current()
        if not person: # its normal here
            self.response.out.write('Nope you won\'t')
            return

        if not users.is_current_user_admin():
            self.response.out.write('Nope you won\'t')
            return

        self.response.out.write('done...')