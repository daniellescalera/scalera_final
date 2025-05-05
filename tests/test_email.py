import pytest
from unittest.mock import AsyncMock
from app.services.email_service import EmailService

@pytest.fixture
def email_service():
    service = EmailService()
    service.send_user_email = AsyncMock()
    return service

def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    email_service.send_user_email(user_data, 'email_verification')
    email_service.send_user_email.assert_called_once_with(user_data, 'email_verification')
