# Base image:
FROM python:3.10-slim

# Set environment variables to reduce Python buffering and enable Docker logs to display in real-time.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for psycopg2 and other Python packages that may need compilation.
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client build-essential libpq-dev && \
    # Clean up the apt cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app/

# Copy only the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the templates directory into the container at /app/templates
COPY templates /app/templates

# Copy your application's entry point script
COPY application.py /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run application.py when the container launches
CMD ["python", "application.py"]
