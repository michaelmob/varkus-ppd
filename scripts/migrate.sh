#!/bin/bash
cd "${0%/*}"
./manage.sh makemigrations
./manage.sh migrate