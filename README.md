# Castlab Proxy

Simple proxy for castlabs

## Description

A proxy that add a authentification token to all post request and forward the request to a custom target.

## Getting Started

### How does the proxy works?

* POST requests are forwarded to the settings.PROXY_ENDPOINT value
* GET /status requests display the current proxy status
* All GET request that are not /status answer with an 404 error
* The proxy run inside a docker container with default host port 8080. You can change the host port with make run HTTP_PORT.
* The proxy listen inside the container at the specified port at settings.PROXY_PORT

### Dependencies

* Docker version 19.03.12
* docker-compose version 1.27.4
* Python 3.8.2

### Proxy Settings

The proxy running on the container can be configured modfiying the settinds.py

### Executing program

* make help - for targets information
* make build - for building the proxy
* make run [HTTP_PORT] - for starting the proxy
* make test - if you want to launch the test after modifying the code

### Debugging

The proxy logs at the standard output, so you can see the logs with docker logs.

When you run the tests with "make test", if a test fails, you will not be able to
see the docker logs since the container is destroyed after the testing phase. For
that reason use "make test-debug" and the container will not be destroyed so
you can access it. Afterwards you can run "make logs" to see the container logs and
"make down"to manually to destroy the container.

Commands:

* make test-debug
* make log
* make down
* make lint => install first flake9

## Authors

Francisco Revilla

## TODO

* Use asynchonous for bonus point.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE] License - see the LICENSE.md file for details
