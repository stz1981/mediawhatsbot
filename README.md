# WhatsApp Media Downloader Bot 🎥🎵

This project is a WhatsApp bot that allows users to download audio and video from YouTube links using the WhatsApp Business API Sandbox by Meta. The bot can also register user interest and send emails with user details.

## Features ✨
- Download audio or video from YouTube links.
- Ensure the file size does not exceed 50MB.
- Register user interest and send details via email.
- Hosted in a Docker container for easy deployment.

## Prerequisites 📋
- Docker and Docker Compose installed.
- Meta for Developers account.
- WhatsApp Business API Sandbox setup.

## Setup Instructions 🛠️

### 1. Clone the Repository
```bash
git clone https://github.com/stz1981/whatsapp-bot.git
cd whatsapp-bot
```

### 2. Set Up Meta for Developers
1. Go to the Meta for Developers website.
2. Sign in with your Facebook account.
3. Create a new app by navigating to "My Apps" and clicking "Create App".
4. Choose the "Business" type and follow the prompts to create your app.
5. Add the WhatsApp product to your app and follow the setup instructions.
6. Note down your **Temporary Access Token**, **Phone Number ID**, and **WhatsApp Business Account ID**.

### 3. Update Environment Variables
Update the `docker-compose.yaml` file with your credentials:
```yaml
environment:
  - FLASK_ENV=development
  - SECRET_KEY=your_secret_key
  - ACCESS_TOKEN=your_temporary_access_token
  - PHONE_NUMBER_ID=your_phone_number_id
  - EMAIL_USER=your_email@gmail.com
  - EMAIL_PASS=your_email_password
```

### 4. Build and Run the Docker Container 🐳
```bash
docker-compose up --build
```

### 5. Interact with the Bot 🤖
Send a WhatsApp message to your sandbox number to start interacting with the bot. The bot will guide you through downloading audio or video from YouTube links and registering your interest.

## Directory Structure 📂
```
whatsapp-bot/
├── app/
│   ├── bot.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yaml
└── volumes/
    ├── Audio/
    └── Video/
```

## Bot Script Overview 📜

### `app/bot.py`
This script handles the bot logic, including downloading media, sending WhatsApp messages, and registering user interest.

### `app/requirements.txt`
Lists the required Python packages.

### `app/Dockerfile`
Defines the Docker image, including installing `ffmpeg` and `ffprobe`.

### `docker-compose.yaml`
Configures the Docker services and environment variables.

## Contributing 🤝
Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License 📄
This project is licensed under the MIT License.

---

Happy coding! 🚀
