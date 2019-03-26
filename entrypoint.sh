#!/bin/bash

exec gunicorn --chdir project app:app --keep-alive 60 --bind 127.0.0.1:5000 --workers 5