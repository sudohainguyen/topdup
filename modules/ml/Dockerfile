# To build TopDup ML Core image
# Base Image
FROM python:3.8.2-buster

# Set default environment variables
ENV PYTHONUNBUFFERED 1 \
    LANG C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Set project environment variables
# Grab these via Python's os.environ
# These are 100% optional here
ENV PYTHONPATH="${PYTHONPATH}:/var/app" \
    LOCAL_DB_URI=sqlite:////artifacts/local.db \
    CAND_PATH=/artifacts/cand.bin \
    RTRV_PATH=/artifacts/rtrv.bin \
    LOCAL_IDX_PATH=/artifacts/local_index.bin \
    REMOTE_IDX_PATH=/artifacts/remote_index.bin

# Create and set working directory
RUN mkdir -p /var/app/modules/ml
WORKDIR /var/app/modules/ml

# Add current directory code to working directory
COPY modules/ml/ .

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    tzdata && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run the Python task
WORKDIR /var/app
CMD ["python", "modules/ml/cronjobs.py"]
