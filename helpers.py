"""Helpers for twitter app."""

from google.appengine.ext import ndb


class Settings(ndb.Model):
    """Models an individual Settings entry."""

    consumer_key = ndb.StringProperty()
    consumer_secret = ndb.StringProperty()
    access_token_key = ndb.StringProperty()
    access_token_secret = ndb.StringProperty()


def get_settings():
    """Return the config settings."""
    key = ndb.Key('Settings', 'config')
    config = key.get()
    settings = {
        'consumer_key': config.consumer_key,
        'consumer_secret': config.consumer_secret,
        'access_token_key': config.access_token_key,
        'access_token_secret': config.access_token_secret,
    }
    return settings
