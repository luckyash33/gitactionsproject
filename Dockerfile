# Aviz Academy - Batch 8 | DevSecOps Training
# Multi-stage build is overkill for a simple app, so keeping it clean and simple
# Using slim variant = smaller image = smaller attack surface (fewer CVEs)

FROM python:3.12-slim

# Metadata labels — good practice, helps identify images in Docker Hub
LABEL maintainer="avizacademy.com"
LABEL batch="batch-8"
LABEL description="Aviz Academy GitHub Actions demo app"

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker layer caching
# If requirements.txt hasn't changed, this layer is reused (faster builds)
COPY requirements.txt .

# Install dependencies
# --no-cache-dir = don't store pip cache inside image (keeps image smaller)
# --upgrade pip  = avoid pip vulnerability warnings
RUN pip install --no-cache-dir pip==24.3.1 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create a non-root user — security best practice
# Running as root inside a container is a HIGH severity finding in Trivy
RUN adduser --disabled-password --gecos "" avizuser
USER avizuser

# Document the port (doesn't actually publish it — that's done at runtime)
EXPOSE 5000

# Health check — Docker will mark container as unhealthy if this fails
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Use gunicorn for production — NOT flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
