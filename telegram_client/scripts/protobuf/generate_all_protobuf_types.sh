#!/bin/bash

cd /protobuf_types/
protoc --python_out=. *.proto
