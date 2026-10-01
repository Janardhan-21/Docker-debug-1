FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies first for better Docker layer caching
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]