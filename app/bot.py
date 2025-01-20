from flask import Flask, request, session, jsonify
import yt_dlp
import os
import re
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# WhatsApp API credentials
ACCESS_TOKEN = 'your_temporary_access_token'
PHONE_NUMBER_ID = 'your_phone_number_id'

# Function to send WhatsApp message
def send_whatsapp_message(to, message):
    url = f" https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to download video or audio
def download_media(url, media_type):
    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '/app/Audio/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'noplaylist': True,
            'max_filesize': 50 * 1024 * 1024,  # 50MB
        }
    else:
        ydl_opts = {
            'format': 'b[filesize<50M] / w',
            'outtmpl': '/app/Video/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'noplaylist': True,
            'max_filesize': 50 * 1024 * 1024,  # 50MB
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_name = ydl.prepare_filename(info_dict)
    return file_name

# Function to send email
def send_email(subject, body, to_email):
    from_email = 'your_email@gmail.com'
    password = 'your_email_password'
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.json.get('messages')[0].get('text').get('body').strip()
    from_number = request.json.get('messages')[0].get('from')
    
    if 'http' in incoming_msg:
        send_whatsapp_message(from_number, "Would you like to download the audio or video? Reply with 'audio' or 'video'. You can also register your interest by replying with 'register'.")
        session['url'] = incoming_msg
    elif incoming_msg.lower() in ['audio', 'video']:
        url = session.get('url')
        if url:
            try:
                file_name = download_media(url, incoming_msg.lower())
                send_whatsapp_message(from_number, f"Here is your {incoming_msg.lower()} file: {file_name}")
            except yt_dlp.utils.DownloadError:
                send_whatsapp_message(from_number, "The file size exceeds 50MB. Please visit https://utube.bayt.cc for larger files.")
        else:
            send_whatsapp_message(from_number, "Please send a valid URL first.")
    elif incoming_msg.lower() == 'register':
        send_whatsapp_message(from_number, "Please provide your name.")
        session['register'] = True
    elif session.get('register'):
        if 'name' not in session:
            session['name'] = incoming_msg
            send_whatsapp_message(from_number, "Please provide your email address.")
        elif 'email' not in session:
            email = incoming_msg
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                session['email'] = email
                user_details = f"Name: {session['name']}\nEmail: {session['email']}\nMessage: {session.get('message', 'No message provided')}"
                send_email("User Registration", user_details, "talal.zaki@gmail.com")
                send_whatsapp_message(from_number, "Thank you for registering your interest. We will get back to you soon.")
                session.pop('register', None)
                session.pop('name', None)
                session.pop('email', None)
            else:
                send_whatsapp_message(from_number, "Invalid email format. Please provide a valid email address.")
    else:
        send_whatsapp_message(from_number, "Welcome to the YouTube Downloader Bot! Send me a YouTube link to get started.")

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
