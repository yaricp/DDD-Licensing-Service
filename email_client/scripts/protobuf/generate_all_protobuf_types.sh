#!/bin/bash

cd email_client/protobuf_types/
protoc --python_out=. *.proto