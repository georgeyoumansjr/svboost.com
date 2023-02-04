from email.mime.text import MIMEText
import google_auth_oauthlib.flow
from flask import request, redirect, session, url_for
import os, sys
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """

    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body


def send_message(service, message, user_id = 'me'):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return 'Message sent'
    except Exception as e:
        print("Error " + str(e))
        return "Error " + str(e)


def build_service_message(creds):
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_stored_credential(token_filename, scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_filename):
        creds = Credentials.from_authorized_user_file(token_filename, scopes)

    print(token_filename)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(">> creds is not valid or has expired")
            creds.refresh(Request())


    return creds

from config.config import EMAIL
from config.config import ROOT
def send_email_helper(subject, message_body, to=EMAIL):
    message = create_message(sender='me', to=to, subject=subject, message_text=message_body)
    print(ROOT+'/token.json')
    creds = get_stored_credential(token_filename=ROOT+'/token.json', scopes=['https://www.googleapis.com/auth/gmail.send'])
    if creds is not None:
        service = build_service_message(creds=creds)
        response = send_message(service=service, message=message)
    else:
        response = 'Fail when loading credentials'
    return response