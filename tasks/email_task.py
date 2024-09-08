from errors.exception_classes import EmailSenderError
from email.message import EmailMessage
from utils.celery_config import app
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()


@app.task
def mail_sender(
        html_template: str,
        email_subject: str,
        receiver_email: str
) -> None:
    message = EmailMessage()

    sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_smtp = "smtp.gmail.com"

    if not sender_email_address or not email_password:
        raise ValueError("Sender email address or email password is not set in environment variables")

    message["Subject"] = email_subject
    message["From"] = sender_email_address
    message["To"] = receiver_email

    message.add_alternative(html_template, subtype="html")
    try:
        with smtplib.SMTP(email_smtp, 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email_address, email_password)
            server.send_message(message)

    except Exception as e:
        raise EmailSenderError(detail=e) from e
