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
# Install Maxmind GeoIP Database
sudo add-apt-repository ppa:maxmind/ppa
sudo apt update

# Install required packages 
sudo apt install -y \
	sudo \
	git \
	build-essential \
	python3-dev \
	python3-setuptools \
	python-virtualenv \
	postgresql \
	postgresql-contrib \
	libpq-dev \
	redis-server \
	rabbitmq-server \
	postfix \
	nginx \
	software-properties-common \
	libmaxminddb0 \
	libmaxminddb-dev \
	mmdb-bin
```
2. Git clone this repository on the server into "/var/www/".

#### Step 2: PostgreSQL Setup
1. Create a user for your database. ```sudo -u postgres createuser -D -A -P $USER```
2. Create a database for Viking and give user full access. ```sudo -u postgres createdb -O $USER $DATABASE```

#### Step 3: Setup Environment
1. Create a virtual environment in the Viking directory. ```virtualenv -p $(which python3) env```

#### Step 4: Django Setup
1. Remove underscore from "project/viking/\_private" directory.
2. Make all required changes in renamed "private" directory. (PostgreSQL details)
3. Navigate to "scripts/" directory.
4. Run "./viking geoip".
5. Run "./manage makemigrations" and "./manage migrate" (Verify that "axes" table was created.)
6. Modify DEBUG in settings_com.py to set debug.

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
4. Navigate to `/opt/letsencrypt/`
5. Run LetsEncrypt **(Replace viking.com with your domain)** ```./letsencrypt-auto certonly -a webroot --webroot-path=/var/www/viking -d viking.com -d www.viking.com```
6. Generate dh group ```openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048```
7. Modify Viking's NGiNX config to point to these certs and uncomment all SSL options.

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