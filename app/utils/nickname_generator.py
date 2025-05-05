from builtins import str

def generate_nickname(email: str) -> str:
    """
    Generate a nickname based on the email address.
    Example: "jsmith@example.com" -> "jsmith"
    """
    return email.split('@')[0]
