FROM python:3.12-slim

WORKDIR /app

COPY . .

# Install ffmpeg and ffprobe
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

#Create download folder where audio and videos will be downloaded
VOLUME ["/app/Audio", "/app/Video"]

#Run the script
CMD ["python", "bot.py"]
