# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies (optionnel mais recommandé)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
# Le context est à la racine (..), donc pas besoin de ../
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Create data and logs directories (sans copier le contenu, on utilise des volumes)
RUN mkdir -p /app/data /app/logs

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Command to run the pipeline
CMD ["python", "-m", "src.main"]