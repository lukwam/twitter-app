#!/usr/bin/env python
"""BITSdb App main."""

import jinja2
import os
import webapp2

# from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
# from google.cloud import datastore

import google.auth
import helpers

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


credentials, project_id = google.auth.default()

def is_dev():
    """Return true if this is the development environment."""
    dev = False
    if os.environ['SERVER_SOFTWARE'].startswith('Development'):
        dev = True
    return dev


def render_theme(body):
    """Render the main template header and footer."""
    template = JINJA_ENVIRONMENT.get_template('theme.html')
    return template.render(
        body=body,
        email=users.get_current_user().email(),
        is_admin=users.is_current_user_admin(),
        is_dev=is_dev(),
    )


class AdminPage(webapp2.RequestHandler):
    """Admin page class."""

    def get(self):
        """Return content for admin page."""
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        template_values = {}
        body = template.render(template_values)
        self.response.write(render_theme(body=body))


class MainPage(webapp2.RequestHandler):
    """MainPage class."""

    def get(self):
        """Return content for main page."""
        template = JINJA_ENVIRONMENT.get_template('index.html')
        template_values = {}
        body = template.render(template_values)
        self.response.write(render_theme(body=body))


class SettingsPage(webapp2.RequestHandler):
    """SettingsPage class."""

    def get(self):
        """Return content for settings page."""
        # get settings from datastore
        params = helpers.get_settings()
        template = JINJA_ENVIRONMENT.get_template('settings.html')
        body = template.render(**params)
        self.response.write(render_theme(body=body))

    def post(self):
        """Return content for settings page."""
        # get settings from post data
        post_data = self.request.POST
        consumer_key = post_data.get('consumer_key')
        consumer_secret = post_data.get('consumer_secret')
        access_token_key = post_data.get('access_token_key')
        access_token_secret = post_data.get('access_token_secret')

        # create entity
        entity = helpers.Settings(
            id='config',
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
        )

        # save entity
        entity.put()

        template = JINJA_ENVIRONMENT.get_template('settings.html')
        body = template.render(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
        )
        self.response.write(render_theme(body=body))


class UpdatePage(webapp2.RequestHandler):
    """UpdatePage class."""

    def get(self):
        """Return content for update page."""
        # get settings from datastore
        settings = helpers.get_settings()
        template = JINJA_ENVIRONMENT.get_template('settings.html')
        body = template.render()
        self.response.write(render_theme(body=body))


app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/admin', AdminPage),
    (r'/admin/settings', SettingsPage),
    (r'/admin/update', UpdatePage)
], debug=True)
