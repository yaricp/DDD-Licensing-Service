#!/bin/bash

cd backend/licensing_service/infra/protobuf_types/
protoc --python_out=. *.proto