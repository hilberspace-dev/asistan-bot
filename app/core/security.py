"""
Security utilities for encryption and password hashing
"""
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from typing import Optional
import base64
import os


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EncryptionManager:
    """Manages encryption/decryption of sensitive data like API keys"""
    
    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize encryption manager
        
        Args:
            encryption_key: Base64 encoded Fernet key. If None, generates a new one.
        """
        if encryption_key:
            self.key = encryption_key.encode()
        else:
            # Generate a new key
            self.key = Fernet.generate_key()
        
        self.fernet = Fernet(self.key)
    
    def get_key(self) -> str:
        """Get the encryption key as a string"""
        return self.key.decode()
    
    def encrypt(self, plain_text: str) -> str:
        """
        Encrypt plain text
        
        Args:
            plain_text: Text to encrypt
            
        Returns:
            Encrypted text as a string
        """
        if not plain_text:
            return ""
        
        encrypted = self.fernet.encrypt(plain_text.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt encrypted text
        
        Args:
            encrypted_text: Encrypted text
            
        Returns:
            Decrypted plain text
        """
        if not encrypted_text:
            return ""
        
        decrypted = self.fernet.decrypt(encrypted_text.encode())
        return decrypted.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


# Global encryption manager instance
# In production, load the key from environment variable
encryption_manager = EncryptionManager()
