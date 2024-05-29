FROM python:slim

# Uprade pip
RUN pip3 install --upgrade pip

# Install requirements
COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY app /app

EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]