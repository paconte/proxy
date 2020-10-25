# set base image (host OS)
FROM python:3.8

# set the working directory in the container
RUN mkdir -p /opt/proxy
COPY . /opt/proxy

# install dependencies
WORKDIR /opt/proxy
RUN pip3 install -r requirements.txt

# command to run on container start
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/proxy/proxy
CMD [ "python", "proxy.py" ]