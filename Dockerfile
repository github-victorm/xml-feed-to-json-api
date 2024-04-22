# Use Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if any are needed
RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security purposes
RUN useradd -m myuser
USER myuser

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY --chown=myuser:myuser . .

# Define the port on which the container should listen
EXPOSE 8080

# Start the application using Flask's built-in server
CMD ["python", "main.py"]