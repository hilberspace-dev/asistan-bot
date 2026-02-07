"""
Tenant (Müşteri) Model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base
from app.core.security import encryption_manager


class Tenant(Base):
    """
    Tenant model representing a customer (Müşteri)
    Each tenant has their own Virtual Receptionist configuration
    """
    
    __tablename__ = "tenants"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Authentication
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Business Information
    business_name = Column(String(255), nullable=False)
    
    # OpenAI Configuration (Encrypted)
    openai_api_key = Column(Text, nullable=False)  # Stored encrypted
    
    # Bot Configuration
    system_prompt = Column(Text, nullable=False, default="Sen bir sanal resepsiyonistsin.")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, username='{self.username}', business='{self.business_name}')>"
    
    def set_openai_api_key(self, plain_api_key: str) -> None:
        """
        Set OpenAI API key (automatically encrypts it)
        
        Args:
            plain_api_key: Plain text API key
        """
        self.openai_api_key = encryption_manager.encrypt(plain_api_key)
    
    def get_openai_api_key(self) -> str:
        """
        Get decrypted OpenAI API key
        
        Returns:
            Decrypted API key
        """
        return encryption_manager.decrypt(self.openai_api_key)
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert tenant to dictionary
        
        Args:
            include_sensitive: Whether to include API key (decrypted)
            
        Returns:
            Dictionary representation
        """
        data = {
            "id": self.id,
            "username": self.username,
            "business_name": self.business_name,
            "system_prompt": self.system_prompt,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_sensitive:
            data["openai_api_key"] = self.get_openai_api_key()
        
        return data
