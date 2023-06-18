# Use the python:3.10-alpine3.17 image as a base
FROM python:3.10-alpine3.17

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/data

# Install additional dependencies if needed
RUN apk update && apk add --no-cache gcc libc-dev mariadb-dev

# Create a user and set permissions
RUN addgroup -S appuser && adduser -S appuser -G appuser --home /usr/data
RUN chown -R appuser:appuser /usr/data

RUN apk add --no-cache \
    build-base \
    musl-dev \
    python3-dev \
    openblas-dev \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h

# Add the requirements.txt file
COPY ./requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the main.py file
COPY ./devopsproject ./

# Set the user to appuser
USER appuser

# Expose the necessary port
EXPOSE 8000/tcp

# Define the command to run when the container starts
CMD ["gunicorn", "devopsproject.wsgi:application", "--bind", "0.0.0.0:8000"]
