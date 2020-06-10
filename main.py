# -*- coding: utf-8 -*-
"""People App main file."""

import json
import twitter

from flask import Flask, redirect, render_template
from google.cloud import firestore

app = Flask(__name__)


def _get_settings():
    """Return a dict of settings."""
    client = firestore.Client()
    return client.collection("settings").document("twitter").get().to_dict()


def connect():
    settings = _get_settings()
    return twitter.Api(
        consumer_key=settings["consumer_key"],
        consumer_secret=settings["consumer_secret"],
        access_token_key=settings["access_token_key"],
        access_token_secret=settings["access_token_secret"]
    )


def render_theme(body):
    """Return the body rendered in the template theme."""
    return render_template(
        "theme.html",
        body=body,
    )


def save_follower(follower):
    """Save a friend in Firestore."""
    client = firestore.Client()
    index = follower.id_str
    data = follower.AsDict()
    return client.collection("followers").document(index).set(data)


def save_friend(friend):
    """Save a friend in Firestore."""
    client = firestore.Client()
    index = friend.id_str
    data = friend.AsDict()
    return client.collection("friends").document(index).set(data)


@app.route("/")
def index():
    """Return the main Index page."""
    api = connect()
    try:
        user = api.VerifyCredentials()
        print(f"Screen Name: {user.screen_name}")
    except Exception as e:
        print("ERROR: Failed to verify Twitter credentials.")
        return redirect("/auth")

    body = render_template(
        "index.html",
    )
    return render_theme(body)


@app.route("/auth")
def auth():
    """Return the main Index page."""
    api = connect()
    body = render_template(
        "auth.html",
    )
    return render_theme(body)


@app.route("/update/followers")
def update_followers():
    """Update the list of followers."""
    api = connect()
    user = api.VerifyCredentials()

    count = 0
    for follower in api.GetFollowers(user.screen_name):
        count += 1
        save_follower(follower)
        print(f"{count} {follower.screen_name}")

    body = render_template(
        "update_followers.html",
    )
    return render_theme(body)


@app.route("/update/friends")
def update_friends():
    """Update the list of friends."""
    api = connect()
    user = api.VerifyCredentials()

    count = 0
    for friend in api.GetFriends(user.screen_name):
        count += 1
        save_friend(friend)
        print(f"{count} {friend.screen_name}")

    body = render_template(
        "update_friends.html",
    )
    return render_theme(body)


# used for local development
if __name__ == "__main__":
    DEBUG = True

    app.run(host="0.0.0.0", port=8080, debug=DEBUG)
