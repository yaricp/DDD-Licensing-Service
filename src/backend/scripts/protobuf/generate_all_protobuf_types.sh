#!/bin/bash

cd backend/domains/licensing_service/infra/protobuf_types/
protoc --python_out=. *.proto