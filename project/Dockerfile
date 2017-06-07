#
# Dockerfile for Viking
#
FROM python:3.6

RUN echo "2"

# Install Postgres 9.6
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" \
		> /etc/apt/sources.list.d/postgresql.list \
	&& wget --quiet -O - "https://www.postgresql.org/media/keys/ACCC4CF8.asc" | apt-key add - \
	&& apt-get update && apt-get install -y postgresql-9.6

# Directory
RUN mkdir /viking
WORKDIR /viking

# Install pip requirements
ADD requirements.txt /viking
RUN pip install --upgrade pip
RUN pip install -r requirements.txt