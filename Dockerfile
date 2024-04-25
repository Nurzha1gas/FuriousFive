###############################################
# Base Image
###############################################
# Use an official Python runtime as a parent image
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Run the application
CMD ["daphne", "broma_config.asgi:application", "-b", "0.0.0.0", "-p", "$PORT"]



# This Dockerfile sets up a Python-based environment using poetry for dependency management.
# Base Image: Uses python:3.9.5-slim. Configures environment variables for Python and poetry,
# including disabling the pip cache and setting a default timeout for pip operations.
# A 'wait' script is added and made executable to synchronize the container startup in docker-compose.

# Builder Image: Extends the python-base. Installs necessary packages like curl and build-essential for building Python packages.
# Sets up the working directory at PYSETUP_PATH and copies over the poetry configuration files.
# Installs project dependencies via poetry without creating a virtual environment.
# Copies the application code to /app, runs Django migrations, and exposes port 8000 for web access.
