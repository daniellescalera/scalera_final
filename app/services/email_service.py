from fastapi import BackgroundTasks
from pydantic import EmailStr
from app.settings.config import get_settings

settings = get_settings()

class EmailService:
    def __init__(self):
        self.settings = get_settings()

    async def send_verification_email(self, email: EmailStr, token: str):
        # Simulate sending an email (for now)
        print(f"Verification email sent to {email} with token {token}")

def get_email_service():
    return EmailService()
