PYTHON=python3
DOCKERFILE=Dockerfile
IMAGE_NAME=castlab/proxy
APP_NAME=proxy
HTTP_PORT=8080

.PHONY: help clean lint run down build test

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

lint:
	flake8

build:
	@echo "Building..."
	docker-compose build --no-cache
	echo "Building finished."

test:
	@echo "Integration testing ..."
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up -d
	-docker exec ${APP_NAME} bash -c "cd /opt/proxy && python -m unittest"
	docker-compose -p ${APP_NAME} down
	@echo "Integration testing finished."

run:
	#-docker-compose -p ${APP_NAME} down
	#docker-compose -p ${APP_NAME} up
	-docker stop $(APP_NAME);docker rm $(APP_NAME)
	@echo "Starting httpd on host port ${HTTP_PORT}"
	docker run -p ${HTTP_PORT}:8080 --name ${APP_NAME} ${IMAGE_NAME}

run-compose:
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
