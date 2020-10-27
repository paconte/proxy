PYTHON=python3
DOCKERFILE=Dockerfile
IMAGE_NAME=castlab/proxy
APP_NAME=proxy
HTTP_PORT=8080

.PHONY: help clean build test run down up logs

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

lint:
	flake8

build:
	@echo "Building..."
	docker-compose build --no-cache
	echo "Building finished."

test:
	@echo "Testing ..."
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up -d
	-docker exec ${APP_NAME} bash -c "cd /opt/proxy && python -m unittest"
	docker-compose -p ${APP_NAME} down
	@echo "Testing finished."

test-debug:
	@echo "Testing for debugging ..."
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up -d
	docker exec ${APP_NAME} bash -c "cd /opt/proxy && python -m unittest"
	@echo "Testing for debugging finished."

run:
	-docker stop $(APP_NAME);docker rm $(APP_NAME)
	@echo "Starting httpd on host port ${HTTP_PORT}"
	docker run -p ${HTTP_PORT}:8080 --name ${APP_NAME} ${IMAGE_NAME}

up:
	-docker-compose -p ${APP_NAME} down
	docker-compose -p ${APP_NAME} up

down:
	docker-compose -p ${APP_NAME} down

logs:
	docker logs ${APP_NAME}

help:
	@echo ''
	@echo 'Usage: make [TARGET]'
	@echo 'Targets:'
	@echo '  build    	      build docker --image--'
	@echo '  test     	      test docker --container--'
	@echo '  run [HTTP_PORT]     run as service --container--'
	@echo '  clean    	      remove python bytecode'
	@echo '  lint    	      linting with flake8' => flake8 required! => pip install flake8
	@echo ''
