import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")

# ❗ Agar env missing ho to app crash ho (GOOD)
if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_FROM:
    raise RuntimeError("Email environment variables are not set")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fm = FastMail(conf)


async def send_verification_email(email: str, verification_token: str):
    print("EMAIL FUNC CALLED FOR:", email)

    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"""
        <h3>Verify your email</h3>
        <p>Your verification code is: <strong>{verification_token}</strong></p>
        """,
        subtype="html",
    )

    await fm.send_message(message)


async def send_password_reset_email(email: str, reset_token: str):
    reset_url = (
        f"http://127.0.0.1:8000/users/reset-password/?token={reset_token}"
    )

    message = MessageSchema(
        subject="Reset Password",
        recipients=[email],
        body=f"""
        <h3>Reset Password</h3>
        <a href="{reset_url}">Reset Password</a>
        """,
        subtype="html",
    )

    await fm.send_message(message)
