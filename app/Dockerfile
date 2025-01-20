FROM python:3.12-slim

WORKDIR /app

# Install ffmpeg and ffprobe
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

VOLUME ["/app/Audio", "/app/Video"]

CMD ["python", "bot.py"]
