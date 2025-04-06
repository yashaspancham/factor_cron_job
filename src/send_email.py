from pathlib import Path
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
ROOT_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = ROOT_DIR / "credentials" / "credentials.json"
TOKEN_PATH = ROOT_DIR / "credentials" / "token.json"

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def send_email(subject:str,message_text:str)->None:
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    message = create_message(
        sender="yashaspancham@gmail.com",
        to="yashaspancham@gmail.com",
        subject=f"{subject}",
        message_text=f"{message_text}"
    )
    send_result = service.users().messages().send(userId="me", body=message).execute()
    print(f"Email sent! Message ID: {send_result['id']}")
