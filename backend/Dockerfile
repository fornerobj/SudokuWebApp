# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && pip install opencv-python-headless \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the Flask app's port
EXPOSE 8080

# Set the command to run the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

