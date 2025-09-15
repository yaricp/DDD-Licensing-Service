#!/bin/bash

set -e

mkdir -p src/telegram_channel/protobuf_types/
mkdir -p src/email_channel/protobuf_types/
mkdir -p src/backend/domains/licensing_service/infra/protobuf_types/

cp -R src/protobuf_types/* src/telegram_channel/protobuf_types/
cp -R src/protobuf_types/* src/email_channel/protobuf_types/
cp -R src/protobuf_types/* src/backend/domains/licensing_service/infra/protobuf_types/

docker-compose build api
docker-compose build tg
docker-compose build email

