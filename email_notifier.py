import yagmail
import os

def send_email(status, message):

    try:
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        yag = yagmail.SMTP(
            user=smtp_user,
            password=smtp_pass,
            host="smtp-relay.brevo.com",
            port=587
        )

        subject = f"AI News Bot Status: {status}"

        yag.send(
            to=smtp_user,
            subject=subject,
            contents=message
        )

        print("Email sent")
        
    except Exception as e:
        print("Email error:", e)
