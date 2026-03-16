import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(status, message):

    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    subject = f"AI News Bot Status: {status}"

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = smtp_user
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp-relay.brevo.com", 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email sending failed:", e)
