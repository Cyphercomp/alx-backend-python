# Dockerfile

# syntax=docker/dockerfile:1.4

# Base image
FROM python:3.10-slim

# Metadata
LABEL maintainer="Saka Chris <sakachris90@gmail.com>" \
      description="Dockerfile for Django Messaging App" \
      version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
    
# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Collect static files for production
# RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Development: use runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production:
# CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]


# Initial Dockerfile for Django Messaging App

# # Step 1: Using the official Python image
# FROM python:3.10-slim

# # Step 2: Setting environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# # ENV PYTHONDONTWRITEBYTECODE=1
# # ENV PYTHONUNBUFFERED=1

# # Step 3: Setting work directory
# WORKDIR /app

# # Step 4: Installing dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

# # Step 5: Copying project files
# COPY . /app/

# # Step 6: Exposing the port Django runs on
# # EXPOSE 8000

# # Step 7: Running development server
# # CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]