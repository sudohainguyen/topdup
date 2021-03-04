# Base Image
FROM python:3.8

# Set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# Set project environment variables
# Grab these via Python's os.environ
# These are 100% optional here
ENV PORT=8000

# Create and set working directory
RUN mkdir -p /var/app/modules/ml_api
RUN mkdir -p /var/app/modules/ml/document_store

# Add current directory code to working directory
COPY modules/ml_api /var/app/modules/ml_api
COPY modules/ml/document_store/ /var/app/modules/ml/document_store
COPY modules/ml/schema.py /var/app/modules/ml/schema.py
COPY ./Pipfile /var/app/modules/ml_api/Pipfile

# Install system dependencies
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    curl \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv gunicorn uvloop httptools

# Install project dependencies
WORKDIR /var/app/modules/ml_api
RUN pipenv install --skip-lock --system

# Run the API
EXPOSE $PORT
WORKDIR /var/app
RUN export PYTHONPATH=$PYTHONPATH:`pwd`
CMD gunicorn modules.ml_api.main:app --max-requests 100 -b 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker -t 60
