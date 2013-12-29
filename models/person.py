'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import logging
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users


class Person(ndb.Expando):

    registration_date = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def info(self):
        info = PersonInfo.query(ancestor=self.key).get()
        return info

    @classmethod
    def get_current(cls):
        user = users.get_current_user()
        if not user:
            return False
        person = ndb.Key(cls, user.user_id()).get()
        if not person:
            return False
        return person

    @classmethod
    def _to_dict(cls, person):
        person_id = person.key.id()
        person_dict = person.to_dict(
            exclude=[
                'registration_date',
            ]
        )
        person_dict.update({
            'id': person_id,
        })
        return person_dict

    @classmethod
    def _pre_delete_hook(cls, key):
        # This needs fix. Should iterate in memberships as well
        person_info = PersonInfo.query(ancestor=key).get()
        if person_info:
            person_info.key.delete()


class PersonInfo(ndb.Expando):

    creation_date = ndb.DateTimeProperty(auto_now_add=True)
    edit_date = ndb.DateTimeProperty(auto_now=True)
    email = ndb.StringProperty()
    nick_name = ndb.StringProperty()

    @classmethod
    def _to_dict(cls, person_info):
        #person_info_id = person_info.key.id()
        person_info_dict = person_info.to_dict(
            exclude=[
                'creation_date',
                'edit_date',
            ]
        )
        #person_info_dict.update({
            #'id': person_info_id,
        #})
        return person_info_dict
