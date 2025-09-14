#!/bin/bash

docker-compose exec api env PYTHONPATH=$PYTHONPATH:/backend poetry run pytest /backend/domains/licensing_service/tests/unit
docker-compose exec api env PYTHONPATH=$PYTHONPATH:/backend poetry run pytest /backend/domains/licensing_service/tests/integration
