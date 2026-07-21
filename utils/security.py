"""Security Utilities"""
import bcrypt
import secrets
from typing import Optional


def hash_password(password: str) -> str:
    """Hash password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash
    
    Args:
        password: Plain text password
        password_hash: Hashed password
        
    Returns:
        True if password matches
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def generate_token(length: int = 32) -> str:
    """Generate secure random token
    
    Args:
        length: Token length
        
    Returns:
        Random token
    """
    return secrets.token_urlsafe(length)


def validate_api_key(api_key: str, stored_key: str) -> bool:
    """Validate API key
    
    Args:
        api_key: API key to validate
        stored_key: Stored API key hash
        
    Returns:
        True if valid
    """
    return secrets.compare_digest(api_key, stored_key)
