FROM python:3.12-slim

WORKDIR /app

COPY . .

# Install ffmpeg and ffprobe
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip setuptools
RUN pip install -r ./app/requirements.txt


VOLUME ["/app/Audio", "/app/Video"]

CMD ["python", "bot.py"]
