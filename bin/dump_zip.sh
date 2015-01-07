#!/bin/sh
python manage.py dumpdata | gzip > quest_dump.json.gz