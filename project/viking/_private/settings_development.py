# Use below commands to create database
"""
DATABASE_NAME=viking_dev
DATABASE_USER=viking_user
DATABASE_PASS=viking_pass

sudo -u postgres createuser -D -A $DATABASE_USER
sudo -u postgres psql -c "ALTER USER $DATABASE_USER WITH PASSWORD '$DATABASE_PASS';"
sudo -u postgres createdb -O $DATABASE_USER $DATABASE_NAME
"""