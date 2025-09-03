#!/bin/bash

cp -R backend/licensing_service/infra/protobuf_types/* telegram_client/protobuf_types/
cp -R backend/licensing_service/infra/protobuf_types/* email_client/protobuf_types/

docker-compose build api
docker-compose build tg
docker-compose build email

