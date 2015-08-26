# Viking (Varkus)
----
## What is Viking?
Viking is a pay-per-unlock service website.

----

## Production Setup
**In this setup: Ubuntu will be used for the server, MySQL will be used for the database, and NGINX will be used as a reverse-proxy server for Gunicorn.**

#### Step 1: Server Setup
1. Make sure server is up to date. (apt-get update && apt-get upgrade)
2. Install required packages.
```sh
apt-get install git build-essential python3.4-dev mysql-server libmysqlclient-dev memcached rabbitmq-server postfix nginx
```
2. Git clone this repository on the server.

#### Step 2: MySQL Setup
1. Login to MySQL monitor. ```mysql -u root -p```
2. Create a database for Viking. ```CREATE DATABASE {DATABASE_NAME};```
3. Create a new user for new database. ```CREATE USER '{USERNAME}'@'localhost' IDENTIFIED BY '{PASSWORD}';```
4. Give new user privileges on new database. ```GRANT ALL PRIVILEGES ON {DATABASE_NAME}.* TO '{USERNAME}'@'localhost' WITH GRANT OPTION;```

#### Step 3: Django Setup
1. Remove underscore from "project/viking/_private" directory.
2. Make all required changes in renamed "private" directory.
5. Navigate to "project/geoip/" directory.
5. Run "update.sh" script.
3. Navigate to "scripts/" directory.
4. Run "setup" script.