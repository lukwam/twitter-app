#!/bin/sh

gcloud config set project karlsson-twitter

# deploy the app engine app
gcloud -q app deploy app.yaml
