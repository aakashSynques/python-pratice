# app/utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from typing import Optional
import os


# -------------------------
# Token Configuration
# -------------------------
SECRET_KEY = "aakash"  # Just a local secret for your tokens
# 1 day
TOKEN_EXPIRATION = 86400  # 1 day in seconds
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_feedback_token(demo_schedule_id: int) -> str:
    """
    Generate an encrypted token containing only demo_schedule_id.
    """
    data = {"demo_schedule_id": demo_schedule_id}
    return serializer.dumps(data, salt="feedback-link")


def validate_feedback_token(token: str) -> Optional[dict]:
    """
    Validate and decrypt the token.
    Returns the data dict if valid, None if invalid or expired.
    """
    try:
        data = serializer.loads(token, salt="feedback-link", max_age=TOKEN_EXPIRATION)
        return data
    except (BadSignature, SignatureExpired):
        return None


# -------------------------
# AWS SES Email Function
# -------------------------

# Load configuration from environment variables
SMTP_SERVER = os.getenv("AWS_SES_SMTP_SERVER", "email-smtp.ap-south-1.amazonaws.com")
SMTP_PORT = int(os.getenv("AWS_SES_SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("AWS_SES_SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("AWS_SES_SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("FEEDBACK_SENDER_EMAIL", "noreply@synques.net")
SENDER_NAME = os.getenv("FEEDBACK_SENDER_NAME", "Chai ETC Team")


def send_feedback_email(to_email: str, lead_name: str, feedback_url: str) -> bool:
    """
    Send feedback email using AWS SES SMTP.
    """

    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("SES credentials are not configured.")
        return False

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = "Feedback Request"

    body = f"""
Hello {lead_name},

Please click the link below to provide feedback:

{feedback_url}

This link will expire in 1 hour.

Best regards,
Your Company
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print("Email sent via AWS SES successfully!")
        return True
    except Exception as e:
        print(f"Error sending email via AWS SES: {e}")
        return False


def send_feedback_link_for_lead(demo_schedule_id: int, lead_email: str, lead_name: str) -> dict:
    """
    Generate token and send feedback link for a lead demo schedule.
    """
    if not lead_email:
        return {
            "success": False,
            "message": "Lead does not have an email address"
        }

    token = generate_feedback_token(demo_schedule_id)
    # // env se base url le lo, default to localhost if not set
    feedback_url = f"{os.getenv('APP_BASE_URL')}/feedback/{token}"

    email_sent = send_feedback_email(lead_email, lead_name, feedback_url)
    if not email_sent:
        return {
            "success": False,
            "message": "Failed to send email"
        }

    return {
        "success": True,
        "message": "Feedback email sent successfully",
        "feedback_url": feedback_url
    }