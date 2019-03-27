#!/bin/bash

# run migrations
while true; do
    python manage.py db upgrade
    if [ $? -eq 0 ]; then
        break
    fi
    >&2 echo "Upgrade command failed, retrying in 5 secs..."
    sleep 5
done

exec gunicorn --chdir project app:app --keep-alive 60 --bind 0.0.0.0:5000 --workers 2