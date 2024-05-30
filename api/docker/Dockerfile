FROM python:slim

# Uprade pip
RUN pip3 install --upgrade pip

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the files
COPY . .

EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]