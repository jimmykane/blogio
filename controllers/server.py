'''
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
'''
import os
import re
import logging
import config
import webapp2
import jinja2
from models.person import *
from google.appengine.api import users

class RootPage(webapp2.RequestHandler):

    def get(self):
        user = None
        person = None
        user = users.get_current_user()
        if user:
            person = Person.get_current()
        # Left dummy data for usage display
        self._display_root_page(person=person)


    def _display_root_page(self, **kwargs):
        jinja_environment = self.jinja_environment
        app_template = jinja_environment.get_template("/app.html")
        kwargs.update({
            "providers": self._get_providers(),
            "google_analytics_key": self.app.config.get('api_keys').get('google_analytics')
        })
        rendered_app_content = app_template.render(kwargs)
        kwargs.update({"app_content": rendered_app_content})
        self._render_wholepage(**kwargs)
        return True


    def _render_wholepage(self, **kwargs):
        jinja_environment = self.jinja_environment
        template = jinja_environment.get_template("/index.html")
        meta = self._get_project_meta()
        if not "meta" in kwargs:
            kwargs.update({"meta": meta})
        #Get general configuration
        kwargs.update({
            "domain": self.app.config.get("domain_name"),
            "title" : self.app.config.get("project_name"),
            "uri": self.request.uri
        })
        self.response.out.write(template.render(kwargs))
        return True


    def _get_project_meta(self):
        class Expando(object):
            pass
        meta = Expando()
        meta.url = self.request.url
        #Stubs for now
        meta.title = self.app.config.get("project_name")
        meta.description = "Create your own Jukebox, add Youtube songs and listen with friends"
        meta.keywords = "Office jukebox, jukebox, office, youtube"
        meta.image = self.app.config.get('domain_name') + "favicon.png"
        return meta


    def _get_providers(self):
        providers = self.app.config.get("providers")
        providers_list = []
        for name, uri in providers.items():
            providers_list.append({
                "url": users.create_login_url(dest_url="/register/",federated_identity=uri),
                "name": name
            })
        #logging.info(providers_list)
        return providers_list


    @property
    def jinja_environment(self):
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__),
                '../views'
            ))
        )
        return jinja_environment