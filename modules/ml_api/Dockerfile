# Base Image: the core ml image should be uploaded to topdup's registry
FROM hainq15/topdup-ml-core:latest

# Set project environment variables
ENV PORT=8000

# Create and set working directory
RUN mkdir -p /var/app/modules/ml_api

WORKDIR /var/app/modules/ml_api

# Add current directory code to working directory
COPY modules/ml_api .

# Install project dependencies
RUN pip install -r requirements.txt

# Run the API
EXPOSE $PORT
WORKDIR /var/app
RUN export PYTHONPATH=$PYTHONPATH:`pwd`
CMD gunicorn modules.ml_api.main:app --max-requests 100 -b 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker -t 60
