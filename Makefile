PYTHON=python3
DOCKERFILE=Dockerfile
APP_NAME=proxy
HTTP_PORT=8080

.PHONY: clean build test_token build integration_test run stop

all: build test_token

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

lint:
	flake8

unit_test:
	@echo "Unit testing ..."
	${PYTHON} -m unittest test.test_token
	${PYTHON} -m unittest test.test_status
	@echo "Unit testing finished."

build: unit_test stop
	@echo "Building..."
	docker build -t ${APP_NAME} . -f ${DOCKERFILE}
	@echo "Building finished."

integration_test: build
	@echo "Integration testing ..."	
	docker run -d -p 8080:8080 --name ${APP_NAME} ${APP_NAME}
	${PYTHON} -m unittest test.test_proxy
	docker stop $(APP_NAME)
	@echo "Integration testing finished."

run: build
	docker run -p ${HTTP_PORT}:8080 --name ${APP_NAME} ${APP_NAME}
	#${PYTHON} ./proxy/proxy.py ${port}

stop:
	docker stop $(APP_NAME);docker rm $(APP_NAME)
