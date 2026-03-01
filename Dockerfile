FROM python:3.11-slim

# off buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# work directory
WORKDIR /app

# system requirements
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY app ./app
COPY run.py .

# open port
EXPOSE 5000

# gunicorn (production!)
CMD ["gunicorn", "-w", "1", "-k", "gevent", "--worker-connections", "1000","--timeout", "0","-b", "0.0.0.0:5000", "run:app"]
