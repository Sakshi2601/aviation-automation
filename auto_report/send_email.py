import os
import base64
import mimetypes
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Gmail API - send only
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service(credentials_path=None, token_path=None):
    base = os.path.dirname(__file__)
    if not credentials_path:
        credentials_path = os.path.join(base, "config", "credentials.json")
    if not token_path:
        token_path = os.path.join(base, "config", "token.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # save the token
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def create_message_with_attachment(sender, to, subject, message_text, file_path):
    message = EmailMessage()
    message.set_content(message_text)
    message["To"] = to
    message["From"] = sender
    message["Subject"] = subject

    if file_path and os.path.exists(file_path):
        ctype, encoding = mimetypes.guess_type(file_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(file_path, "rb") as f:
            message.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(file_path))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}


def send_report_via_gmail(sender, recipient, subject, body, attachment_path=None, credentials_path=None):
    service = get_gmail_service(credentials_path=credentials_path)
    msg = create_message_with_attachment(sender, recipient, subject, body, attachment_path)
    sent = service.users().messages().send(userId="me", body=msg).execute()
    return sent


if __name__ == "__main__":
    # basic manual test (won't run until you configure credentials.json)
    print("Call send_report_via_gmail(...) with your args to send an email.")