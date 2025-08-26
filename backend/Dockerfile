# Use Python 3.11 slim image (good balance of features and size)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed for your file handlers
# - poppler-utils: for PDF processing
# - libreoffice: for DOCX to PDF conversion (used by docx2pdf)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Command to run when container starts
# For now, we'll just keep the container running for testing
CMD ["python", "-c", "print('Backend container is running...'); import time; time.sleep(3600)"]