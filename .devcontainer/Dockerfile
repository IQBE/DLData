ARG SOURCE=mcr.microsoft.com/vscode/devcontainers/python:3.12
FROM ${SOURCE}
RUN pip3 install --upgrade pip

COPY etl/requirements.txt  /requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive && apt-get -y update; apt-get -y install postgresql-client libproj-dev gdal-bin; apt-get -y clean
RUN pip3 install -r /requirements.txt