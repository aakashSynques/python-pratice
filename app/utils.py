# app/utils.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from typing import Optional

# -------------------------
# Token Configuration
# -------------------------
SECRET_KEY = "your-local-secret-key"  # Just a local secret for your tokens
TOKEN_EXPIRATION = 3600  # 1 hour in seconds
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_feedback_token(lead_id: int, email: str) -> str:
    """
    Generate an encrypted token containing lead_id and email.
    """
    data = {"lead_id": lead_id, "email": email}
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
def send_feedback_email(to_email: str, lead_name: str, feedback_url: str) -> bool:
    """
    Send feedback email using AWS SES SMTP with hardcoded SMTP credentials.
    """

    # --- AWS SES SMTP configuration ---
    SMTP_SERVER = "email-smtp.us-east-1.amazonaws.com"  # Replace with your SES region endpoint
    SMTP_PORT = 587  # TLS
    SMTP_USERNAME = "YOUR_AWS_SMTP_USERNAME"  # Replace with your SMTP username
    SMTP_PASSWORD = "YOUR_AWS_SMTP_PASSWORD"  # Replace with your SMTP password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = "Feedback Request"

    body = f"""
Hello {lead_name},

Please click the link below to provide feedback:

{feedback_url}

This link will expire in 1 hour.

Best regards,
Your Company
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to AWS SES SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        print("Email sent via AWS SES successfully!")
        return True
    except Exception as e:
        print(f"Error sending email via AWS SES: {e}")
        return False