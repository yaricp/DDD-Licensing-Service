#!/bin/bash

export PYTHONPATH="$PYTHONPATH:/backend"

poetry run pytest /backend/licensing_service