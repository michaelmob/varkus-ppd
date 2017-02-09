#
# Dockerfile for Viking
#
FROM python:3.6

RUN mkdir /viking
WORKDIR /viking

# Install pip requirements
ADD requirements.txt /viking
RUN pip install --upgrade pip
RUN pip install -r requirements.txt