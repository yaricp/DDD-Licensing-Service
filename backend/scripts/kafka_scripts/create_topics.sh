#!/bin/bash

docker-compose exec kafka kafka-topics --create --bootstrap-server=localhost:9091 --topic=main-topic