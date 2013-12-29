'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import logging
import hashlib
import json
import webapp2
from controllers.jsonhandler import *
from models.person import *
from google.appengine.ext import ndb
from google.appengine.api import users


class LogoutPersonHandler(webapp2.RequestHandler):

    def get(self):
        try:
            return self.redirect(users.create_logout_url(self.request.get('return_url')))
        except Exception as e:
            logging.exception('Could not Logout user\n' + repr(e))
            self.redirect('/')
            return


class RegisterPersonHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri), abort=True)
            return

        person = Person.get_or_insert(user.user_id())
        if not self._register(person, user):
            # more logging is needed
            logging.error('Warning registration failed')
            self.redirect("/")
            return

        self.redirect("/jukeboxes/")

    def post(self):
        self.view("No reason to be here Mr Jiggles ;-)")
        return

    @ndb.transactional(xg=True)
    def _register(self, person, user):

        # Register the info
        person_info = PersonInfo.query(ancestor=person.key).get()
        if not person_info:
            person_info = PersonInfo(id=user.user_id(), parent=person.key)
            person_info.nick_name = user.nickname()
            person_info.email = user.email()
            person_info.put()

        return True


class GetCurrentPersonHanlder(webapp2.RequestHandler, JSONHandler):

    def post(self):
        person = Person.get_current()
        if not person: # its normal here
            response = {'status':self.get_status(status_code=404)}
            self.response.out.write(json.dumps(response))
            return

        # First convert to dict
        person_dict = Person._to_dict(person)
        # Then get info convert to dict and update person dict
        person_info = person.info
        person_info_dict = PersonInfo._to_dict(person_info)
        person_dict.update(person_info_dict)
        response = response = {'data': person_dict}
        response.update({'status': self.get_status()})
        self.response.out.write(json.dumps(response))
