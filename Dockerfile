# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./source ./source
COPY ./target ./target
COPY main.py .
COPY ddl.sql .

# Print Logs instantly
ENV PYTHONUNBUFFERED=1

# Default command to run app
CMD ["python", "main.py"]
