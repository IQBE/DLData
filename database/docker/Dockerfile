FROM python:slim

# Uprade pip
RUN pip3 install --upgrade pip

# Install requirements
COPY requirements.txt /database/
WORKDIR /database
RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY alembic.ini .
COPY alembic alembic

CMD [ "alembic", "upgrade", "head" ]