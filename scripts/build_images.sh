#!/bin/bash

set -e

mkdir -p src/telegram_client/protobuf_types/
mkdir -p src/email_client/protobuf_types/
mkdir -p src/backend/licensing_service/infra/protobuf_types/

cp -R src/protobuf_types/* src/telegram_client/protobuf_types/
cp -R src/protobuf_types/* src/email_client/protobuf_types/
cp -R src/protobuf_types/* src/backend/licensing_service/infra/protobuf_types/

docker-compose build api
docker-compose build tg
docker-compose build email

