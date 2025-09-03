#!/bin/bash

echo "start generate all protobuf types"
scripts/protobuf/./generate_all_protobuf_types.sh
echo "finished generate all protobuf types"

export PYTHONPATH="$PYTHONPATH:/pro"
poetry run python /telegram_client/main.py
