#!/bin/sh

# Run alembic migrations
alembic upgrade head

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 7000 --workers 2 &

# Keep the script running
wait
