#!/bin/bash

cd telegram_client/protobuf_types/
protoc --python_out=. *.proto