import os
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib

load_dotenv()


def recover_password(email_subject: str, receiver_email: str):
    message = EmailMessage()

    sender_email_address = os.getenv("SENDER_EMAIL_ADDRESS")
    email_smtp = "smtp.gmail.com"
    email_password = os.getenv("EMAIL_PASSWORD")

    message["Subject"] = email_subject
    message["From"] = sender_email_address
    message["To"] = receiver_email

    message.set_content("Hola amigo dev de Marvic")
    server = smtplib.SMTP(email_smtp, 587)

    server.ehlo()
    server.starttls()

    server.login(sender_email_address, email_password)
    server.send_message(message)

    server.quit()
