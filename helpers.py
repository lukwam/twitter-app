"""Helpers for twitter app."""

from google.appengine.ext import ndb

import twitter

class Settings(ndb.Model):
    """Models an individual Settings entry."""

    consumer_key = ndb.StringProperty()
    consumer_secret = ndb.StringProperty()
    access_token_key = ndb.StringProperty()
    access_token_secret = ndb.StringProperty()

class Twitter(object):
    """Twitter class."""

    def __init__(self):
        """Iniatiator funciton."""
        self.api = twitter.Api(**get_settings())
        self.user = self.api.VerifyCredentials()

    def get_friends(self, user):
        """Return a list of friends."""
        friends = []
        for user in self.api.GetFriends(user):
            user = user.AsDict()
            uid = user['id']
            key = ndb.Key('Friend', uid)
            entity = datastore.Entity(key)
            entity['screen_name'] = user['screen_name']
            for k in user:
                if k in [
                    'status',
                ]:
                    continue
                entity[k] = user[k]
            friends.append(entity)
        return friends

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
