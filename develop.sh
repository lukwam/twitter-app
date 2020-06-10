#!/bin/bash

# PROJECT="lukwam-twitter"
# REPO="twitter-app"
# IMAGE="gcr.io/${PROJECT}/${REPO}:latest"
IMAGE="twitter-app"

SERVICEACCOUNT="service_account.json"

# pull the newest image
# docker pull ${IMAGE}

docker run -it --rm \
  --expose 8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS="/usr/src/etc/${SERVICEACCOUNT}" \
  -p 8080:8080 \
  -v "$(pwd)":/usr/src \
  -w /usr/src \
  ${IMAGE} \
  python main.py
