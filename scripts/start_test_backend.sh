#!/bin/bash

docker-compose exec api env PYTHONPATH=$PYTHONPATH:/backend poetry run pytest /backend/licensing_service/tests/unit
