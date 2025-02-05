# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /exchanger

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements/prod.txt

# Copy project files into the container
COPY . /exchanger/

# For production you might use gunicorn; for local development we use Django's runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
