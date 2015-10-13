# Viking (Varkus)
----
## What is Viking?
Viking is a pay-per-unlock service website.

----

## Production Setup
**In this setup: Ubuntu will be used for the server, PostgreSQL will be used for the database, and NGINX will be used as a reverse-proxy server for Gunicorn.**

#### Step 1: Server Setup
1. Make sure server is up to date. (apt-get update && apt-get upgrade)
2. Install required packages.
```sh
apt-get install git build-essential python3-dev postgresql postgresql-contrib libpq-dev memcached rabbitmq-server postfix nginx libjpeg8-dev
```
2. Git clone this repository on the server into "/var/www/".

#### Step 2: PostgreSQL Setup
1. Create a user for your database. ```sudo -u postgres createuser -D -A -P {USERNAME}```
2. Create a database for Viking and give user full access. ```sudo -u postgres createdb -O {USERNAME} {DATABASE_NAME}```

#### Step 3: Django Setup
1. Remove underscore from "project/viking/_private" directory.
2. Make all required changes in renamed "private" directory. (PostgreSQL details)
3. Navigate to "project/geoip/" directory.
4. Run "update.sh" script.
5. Navigate to "scripts/" directory.
6. Run "setup" script.

#### Step 4: Setup Nginx
1. Navigate to "/etc/nginx/sites-available".
2. Create a new file and symlink it to sites-enabled or you can edit "default" file.
3. In that file, an example can be found in "_private/nginx.example".

#### Step 5: Run at Startup (Optional)
1. Edit /etc/local.rc
2. Modify and add the below code before "exit 0".

```sudo -u {USERNAME} /var/www/viking/scripts/viking start```