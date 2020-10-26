PYTHON=python3
DOCKERFILE=Dockerfile
IMAGE_NAME=castlab/proxy
APP_NAME=proxy
HTTP_PORT=8080

.PHONY: help clean lint run down build unit_test integration_test

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

lint:
	flake8

build:
	@echo "Building..."
	docker-compose build --no-cache
	echo "Building finished."

unit_test:
	@echo "Unit testing ..."
	${PYTHON} -m unittest test.test_token
	${PYTHON} -m unittest test.test_status
	@echo "Unit testing finished."

integration_test: unit_test
	@echo "Integration testing ..."
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up -d
	-${PYTHON} -m unittest test.test_proxy
	docker-compose -p ${APP_NAME} down
	@echo "Integration testing finished."

test: integration_test

run:
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up

down:
	docker-compose -p ${APP_NAME} down

help:
	@echo ''
	@echo 'Usage: make [TARGET]'
	@echo 'Targets:'
	@echo '  build    	build docker --image--'
	@echo '  test     	test docker --container--'
	@echo '  run    	run as service --container--'
	@echo '  clean    	remove python bytecode'
	@echo '  lint    	linting with flake8'
	@echo ''
