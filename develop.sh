#!/bin/sh

APP='karlsson-twitter'

sudo docker run -it --rm \
  -v /etc/localtime:/etc/localtime:ro \
  -v "$(pwd):/usr/src" \
  -v /local/datastore:/local/datastore:rw \
  -v "$(pwd)/tmp:/tmp:rw" \
  --expose 8000 \
  --expose 8080 \
  -p 8000:8000 \
  -p 8080:8080 \
  -w /usr/src \
  google/cloud-sdk:latest \
    dev_appserver.py \
      -A ${APP} \
      --admin_host 0.0.0.0 \
      --admin_port 8000 \
      --appidentity_email_address=${APP}@appspot.gserviceaccount.com \
      --appidentity_private_key_path=service_account.pem \
      --api_port 8081 \
      --datastore_path /local/datastore/${APP} \
      --host 0.0.0.0 \
      --port 8080 \
      --enable_host_checking false \
      --skip_sdk_update_check true \
      --use_mtime_file_watcher true \
      app.yaml
      # --clear_datastore
