ARG SOURCE=mcr.microsoft.com/vscode/devcontainers/python:3.12
FROM ${SOURCE}
RUN pip3 install --upgrade pip

RUN export DEBIAN_FRONTEND=noninteractive && apt-get -y update; apt-get -y install postgresql-client libproj-dev gdal-bin; apt-get -y clean

# Install invoke
RUN pip3 install invoke

# Install etl Python dependencies
COPY etl/requirements.txt etl/requirements-dev.txt  /
RUN pip3 install -r /requirements.txt
RUN pip3 install -r /requirements-dev.txt

# Install api Python dependencies
COPY api/requirements.txt /
RUN pip3 install -r /requirements.txt