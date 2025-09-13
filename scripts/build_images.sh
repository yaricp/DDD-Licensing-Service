#!/bin/bash

cp -R src/backend/licensing_service/infra/protobuf_types/* src/telegram_client/protobuf_types/
cp -R src/backend/licensing_service/infra/protobuf_types/* src/email_client/protobuf_types/

docker-compose build api
docker-compose build tg
docker-compose build email

