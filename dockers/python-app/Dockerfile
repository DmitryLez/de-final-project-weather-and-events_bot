# Dockerfile
FROM python:3.11

WORKDIR /app

# Copy requirements file if you have one
COPY requirements.txt .

# Install necessary Python packages
RUN pip install  -r requirements.txt

# Example command to run the Python application
CMD ["python", "-m", "http.server", "8000"]

