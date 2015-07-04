sudo apt-get install \
	build-essential \
	libmysqlclient-dev \
	python3.4-dev \
	python-magic \
	rabbitmq-server

./pip.sh install -r "$(pwd)/requirements.txt"