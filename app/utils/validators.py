from builtins import bool, str
from email_validator import validate_email as external_validate_email, EmailNotValidError
from urllib.parse import urlparse

def validate_email_address(email: str) -> bool:
    """
    Validate the email address using the email-validator library.
    
    Args:
        email (str): Email address to validate.
    
    Returns:
        bool: True if the email is valid, otherwise False.
    """
    try:
        external_validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False

# Alias to match test expectation
validate_email = validate_email_address

def validate_url(url: str) -> bool:
    """
    Validate that the URL starts with http:// or https:// and has a network location.
    
    Args:
        url (str): URL to validate.
    
    Returns:
        bool: True if the URL is valid, otherwise False.
    """
    parsed = urlparse(url)
    return parsed.scheme in ["http", "https"] and bool(parsed.netloc)
