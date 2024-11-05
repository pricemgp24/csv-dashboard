# Dockerfile for Backend
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask API
EXPOSE 5000

# Set environment variables to prevent Python from writing .pyc files and to enable buffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the command to start the Flask server
CMD ["python", "app.py"]
