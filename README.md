# Viking (Varkus)
----
## What is Viking?
Viking is a pay-per-unlock service website.

----

## Production Setup
**In this setup: Ubuntu will be used for the server, PostgreSQL will be used
for the database, and NGINX will be used as a reverse-proxy server for Daphne.**

#### Step 1: Server Setup
1. Make sure server is up to date. (sudo apt update && sudo apt upgrade)
2. Install required packages.
```
apt update && apt install -y sudo software-properties-common && add-apt-repository -y ppa:maxmind/ppa && apt update && apt install -y git build-essential python3-dev python3-setuptools python-virtualenv postgresql postgresql-contrib libpq-dev redis-server rabbitmq-server postfix nginx libmaxminddb0 libmaxminddb-dev mmdb-bin
```
2. Git clone this repository on the server into "/var/www/".

#### Step 2: PostgreSQL Setup
1. Create a user for your database. ```sudo -u postgres createuser -D -A $DB_USER```
2. Set your database user's password. ```sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';"```
3. Create a database for Viking and give user full access. ```sudo -u postgres createdb -O $DB_USER $DB_NAME```

## Set User to Create Databases for Tests (Optional)  
```sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"```

#### Step 3: Setup Environment
1. Create a virtual environment in the Viking directory. ```virtualenv -p $(which python3) .env```

#### Step 4: Django Setup
1. Copy `exports` file from `project/viking/\_private/` directory to `scripts/` directory.
2. Remove underscore from `project/viking/\_private/` directory.
3. Make all required changes in renamed `private` directory.
4. Navigate to `scripts/` directory.
5. Install Python packages `/viking pip install -r $(pwd)/../project/requirements.txt`
6. Run "./viking geoip".
7. Run "./viking migrate" (Verify that "axes" table was created.)

#### Step 5: Setup Nginx
1. Navigate to "/etc/nginx/sites-available".
2. Create a new file named "viking_com" and symlink it to "/etc/nginx/sites-enabled".
3. In that file make your nginx config. An example can be found in "\_private/nginx.example".

#### Step 5.1: (Optional)
1. Generate or buy an SSL Certificate. ```sudo openssl req -x509 -nodes -days 365 -out /etc/ssl/viking.crt -newkey rsa:2048 -keyout /etc/ssl/viking.key```
2. Modify Viking's NGiNX config to point to these certs.

#### Step 5.2: LetsEncrypt (Optional -- preferred)
1. Clone LetsEncrypt repo ```git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt```
2. Create a ".well-known" directory. `mkdir /var/www/viking/.well-known`
3. Uncomment LetsEncrypt section from Viking's NGiNX config.
4. Comment out the Non-SSL server from the NGiNX config and restart it.
5. Navigate to `/opt/letsencrypt/`
6. Run LetsEncrypt **(Replace viking.com with your domain)** ```./letsencrypt-auto certonly -a webroot --webroot-path=/var/www/viking -d viking.com -d www.viking.com```
7. Modify Viking's NGiNX config to point to these certs.
8. Uncomment out the Non-SSL server from the NGiNX config and restart it.
9. Edit crontab. `crontab -e`
10. Add the follow lines for auto-renewal. ```30 2 * * 1 /opt/letsencrypt/letsencrypt-auto renew >> /var/log/le-renew.log
35 2 * * 1 /bin/systemctl reload nginx```

You cannot connect to an insecure websocket from a secure protocol (HTTP !-> HTTPS).
Some provider's (namely AdgateMedia) HTTP notifications/postbacks do not work over HTTPS.
If the above is the case for you, it is recommended to create an insecure subdomain
PRIMARILY for the HTTP notifications/postbacks.

#### Step 6: Run at Startup using Supervisor (Optional)
1. Modify the "viking.conf" file in the "project/viking/\_private/extras/" directory.
2. Copy the file to "/etc/supervisor/conf.d/" directory. **(Set $USER variable!)**
3. Reread supervisor configs ```supervisorctl reread```
4. Update supervisor apps  ```supervisorctl update```
5. Start Viking ```supervisorctl start viking:```