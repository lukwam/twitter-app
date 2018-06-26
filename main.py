#!/usr/bin/env python
"""BITSdb App main."""

import jinja2
import os
import webapp2

# from google.appengine.api import memcache
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


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


app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/admin', AdminPage),
], debug=True)
