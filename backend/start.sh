#!/bin/bash

# echo "Migrations"

# poetry run alembic revision --autogenerate -m 'init'
# poetry run alembic upgrade head

echo "start generate all protobuf types"
scripts/protobuf/./generate_all_protobuf_types.sh
echo "finished generate all protobuf types"

sleep 30

if [[ -z "${HOST}" ]]; then
  HOST="0.0.0.0"
else
  HOST="${HOST}"
fi

if [[ -z "${PORT}" ]]; then
  PORT=8000
else
  PORT="${PORT}"
fi

if [[ -z "${WORKERS}" ]]; then
  WORKERS=4
else
  WORKERS="${WORKERS}"
fi

if [[ -z "${WORKER_CLASS}" ]]; then
  WORKER_CLASS="uvicorn.workers.UvicornWorker"
else
  WORKER_CLASS="${WORKER_CLASS}"
fi

if [[ -z "${LOG_LEVEL}" ]]; then
  LOG_LEVEL="info"
else
  LOG_LEVEL="${LOG_LEVEL}"
fi

if [ "$RELOAD" = true ]; then
  poetry run uvicorn backend.infrastructure.api.main:app --workers $WORKERS --host $HOST --port $PORT --log-level $LOG_LEVEL --reload
else
  poetry run uvicorn backend.infrastructure.api.main:app --workers $WORKERS --host $HOST --port $PORT --log-level $LOG_LEVEL
fi