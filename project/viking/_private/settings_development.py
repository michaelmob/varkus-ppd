# Use below commands to create database
"""
DB_NAME=v_db
DB_USER=v_user
DB_PASS=v_pass

sudo -u postgres createuser -D -A $DB_USER
sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres createdb -O $DB_USER $DB_NAME
"""