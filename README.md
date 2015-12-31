# Viking (Varkus)
----
## What is Viking?
Viking is a pay-per-unlock service website.

----

## Production Setup
**In this setup: Ubuntu will be used for the server, PostgreSQL will be used for the database, and NGINX will be used as a reverse-proxy server for uWSGI.**

#### Step 1: Server Setup
1. Make sure server is up to date. (sudo apt update && sudo apt upgrade)
2. Install required packages.
```

sudo apt install git \
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
	libffi-dev \
	libjpeg8-dev

# Install Maxmind GeoIP Database
sudo add-apt-repository ppa:maxmind/ppa
sudo apt update

sudo apt install libmaxminddb0 \
	libmaxminddb-dev \
	mmdb-bin
```
2. Git clone this repository on the server into "/var/www/".

#### Step 2: PostgreSQL Setup
1. Create a user for your database. ```sudo -u postgres createuser -D -A -P {USERNAME}```
2. Create a database for Viking and give user full access. ```sudo -u postgres createdb -O {USERNAME} {DATABASE_NAME}```

#### Step 3: Setup Environment
1. Create a virtual environment in the Viking directory. ```virtualenv -p /usr/bin/python3 env```

#### Step 4: Django Setup
1. Remove underscore from "project/viking/_private" directory.
2. Make all required changes in renamed "private" directory. (PostgreSQL details)
3. Navigate to "scripts/" directory.
4. Run "setup" and "geoip" script.
5. Run "./manage makemigrations" and "./manage migrate" (Verify that "axes" table was created)

#### Step 5: Setup Nginx
1. Navigate to "/etc/nginx/sites-available".
2. Create a new file and symlink it to sites-enabled or you can edit "default" file.
3. In that file, an example can be found in "_private/nginx.example".

#### Step 6: Run at Startup using SystemD (Optional)
1. Modify the "viking.service" file in the "project/viking/_private" directory.
2. Copy the file to "/etc/systemd/system/" directory.
3. Enable the service ```systemctl enable viking.service```
4. Do the same for the "nginx.service" file.
5. The services will start after you reboot the system.