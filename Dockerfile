#docker run  -d  --net=host --env-file=$(pwd)/keystone.rc --name cap_expoter  os_capacity_expoter
FROM python:2.7-alpine

RUN \
    apk update && \
    apk --no-cache -q add build-base linux-headers libffi-dev openssl-dev python2-dev && \
    pip install -U pip &&\
    pip install python-novaclient python-keystoneclient python-cinderclient \
    prometheus-client requests

ADD expoters /expoters

EXPOSE 8082

CMD ["/usr/local/bin/python", "/expoters/expoter.py"]