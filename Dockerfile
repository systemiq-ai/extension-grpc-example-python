# Dockerfile for the gRPC Publisher Service

# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt first, for better caching
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variable for the environment, default to production
ENV ENVIRONMENT=production

# Unset OTEL_EXPORTER_OTLP_ENDPOINT to prevent OpenTelemetry from using the host's value
ENV OTEL_EXPORTER_OTLP_ENDPOINT=

# Add /app and /app/protos to the PYTHONPATH for module recognition
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/protos"

# Minimize the logging noise
ENV GRPC_VERBOSITY=ERROR

# Expose the standard gRPC port
EXPOSE 50051

# Use JSON format for CMD to prevent OS signal issues
CMD ["/bin/sh", "-c", "if [ \"$ENVIRONMENT\" = \"development\" ]; then \
      echo 'Starting in development mode with auto-reload...' && \
      watchmedo auto-restart --directory=./ --patterns=\"*.py\" --recursive -- python main.py; \
    else \
      echo 'Starting in production mode...' && \
      python main.py; \
    fi"]