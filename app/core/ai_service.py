"""
AI Service for OpenAI Integration
Handles dynamic tenant-based OpenAI API calls with Turkish prompt strategy
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from openai import OpenAI, OpenAIError
import logging

from app.models.tenant import Tenant


# Configure logging
logger = logging.getLogger(__name__)


# Turkish base system prompt that will be prepended to all tenant prompts
TURKISH_BASE_PROMPT = """Sen yardımsever bir Türk asistansın. Adın 'Asistan'. Asla İngilizce cevap verme. Sadece Türkçe konuş. Kısa, net ve samimi ol. Kullanıcının verdiği talimatlara harfiyen uy."""


class AIServiceError(Exception):
    """Custom exception for AI Service errors"""
    pass


class AIService:
    """
    AI Service for handling OpenAI API interactions
    
    This service dynamically initializes OpenAI clients based on tenant configuration,
    ensuring each tenant uses their own API key and system prompt.
    """
    
    def __init__(self, tenant_id: int, db: Session):
        """
        Initialize AI Service for a specific tenant
        
        Args:
            tenant_id: The tenant ID to fetch configuration for
            db: Database session
            
        Raises:
            AIServiceError: If tenant not found or API key not configured
        """
        self.tenant_id = tenant_id
        self.db = db
        self.tenant = self._fetch_tenant()
        self.api_key = self._get_decrypted_api_key()
        self.system_prompt = self._build_system_prompt()
        self.client = self._initialize_client()
    
    def _fetch_tenant(self) -> Tenant:
        """
        Fetch tenant from database
        
        Returns:
            Tenant object
            
        Raises:
            AIServiceError: If tenant not found
        """
        tenant = self.db.query(Tenant).filter(Tenant.id == self.tenant_id).first()
        
        if not tenant:
            logger.error(f"Tenant not found: {self.tenant_id}")
            raise AIServiceError(f"Tenant with ID {self.tenant_id} not found")
        
        logger.info(f"Tenant loaded: {tenant.business_name} (ID: {tenant.id})")
        return tenant
    
    def _get_decrypted_api_key(self) -> str:
        """
        Get and decrypt the tenant's OpenAI API key
        
        Returns:
            Decrypted API key string
            
        Raises:
            AIServiceError: If API key is not configured
        """
        if not self.tenant.openai_api_key:
            logger.error(f"No API key configured for tenant: {self.tenant_id}")
            raise AIServiceError(
                f"OpenAI API key not configured for tenant: {self.tenant.business_name}"
            )
        
        try:
            api_key = self.tenant.get_openai_api_key()
            logger.info(f"API key decrypted successfully for tenant: {self.tenant_id}")
            return api_key
        except Exception as e:
            logger.error(f"Failed to decrypt API key for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"Failed to decrypt API key: {str(e)}")
    
    def _build_system_prompt(self) -> str:
        """
        Build the complete system prompt with Turkish base prompt and tenant-specific instructions
        
        Returns:
            Complete system prompt string
        """
        # Combine Turkish base prompt with tenant's custom prompt
        complete_prompt = f"{TURKISH_BASE_PROMPT}\n\n{self.tenant.system_prompt}"
        
        logger.debug(f"System prompt built for tenant {self.tenant_id}")
        return complete_prompt
    
    def _initialize_client(self) -> OpenAI:
        """
        Initialize OpenAI client with tenant's API key
        
        Returns:
            Configured OpenAI client
            
        Raises:
            AIServiceError: If client initialization fails
        """
        try:
            client = OpenAI(api_key=self.api_key)
            logger.info(f"OpenAI client initialized for tenant: {self.tenant_id}")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def chat_completion(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion using OpenAI API
        
        Args:
            user_message: The user's message
            conversation_history: Optional list of previous messages [{"role": "user/assistant", "content": "..."}]
            model: OpenAI model to use (default: gpt-4o)
            temperature: Response randomness (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            
        Returns:
            Assistant's response text
            
        Raises:
            AIServiceError: If API call fails
        """
        try:
            # Build messages array
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Sending chat completion request for tenant {self.tenant_id}")
            logger.debug(f"Model: {model}, Temperature: {temperature}, Messages: {len(messages)}")
            
            # Make API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            
            logger.info(f"Chat completion successful for tenant {self.tenant_id}")
            logger.debug(f"Response length: {len(assistant_message)} chars")
            
            return assistant_message
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in chat completion for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"Unexpected error: {str(e)}")
    
    def chat_completion_stream(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """
        Generate a streaming chat completion using OpenAI API
        
        Args:
            user_message: The user's message
            conversation_history: Optional list of previous messages
            model: OpenAI model to use (default: gpt-4o)
            temperature: Response randomness (0-2, default: 0.7)
            max_tokens: Maximum tokens in response (optional)
            
        Yields:
            Chunks of assistant's response text
            
        Raises:
            AIServiceError: If API call fails
        """
        try:
            # Build messages array
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            logger.info(f"Sending streaming chat completion request for tenant {self.tenant_id}")
            
            # Make streaming API call
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Yield chunks as they arrive
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            
            logger.info(f"Streaming chat completion completed for tenant {self.tenant_id}")
            
        except OpenAIError as e:
            logger.error(f"OpenAI API error for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in streaming chat completion for tenant {self.tenant_id}: {e}")
            raise AIServiceError(f"Unexpected error: {str(e)}")
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available OpenAI models for this tenant
        
        Returns:
            List of model names
        """
        # Common GPT models
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo"
        ]
    
    def validate_api_key(self) -> bool:
        """
        Validate that the tenant's API key is working
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Make a minimal API call to test the key
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            logger.info(f"API key validated successfully for tenant {self.tenant_id}")
            return True
        except OpenAIError as e:
            logger.warning(f"API key validation failed for tenant {self.tenant_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating API key for tenant {self.tenant_id}: {e}")
            return False
    
    def get_tenant_info(self) -> Dict[str, any]:
        """
        Get tenant information
        
        Returns:
            Dictionary with tenant details
        """
        return {
            "tenant_id": self.tenant.id,
            "business_name": self.tenant.business_name,
            "username": self.tenant.username,
            "has_api_key": bool(self.tenant.openai_api_key),
            "system_prompt_length": len(self.tenant.system_prompt),
            "created_at": self.tenant.created_at.isoformat() if self.tenant.created_at else None
        }


def create_ai_service(tenant_id: int, db: Session) -> AIService:
    """
    Factory function to create an AI Service instance
    
    Args:
        tenant_id: The tenant ID
        db: Database session
        
    Returns:
        Configured AIService instance
        
    Raises:
        AIServiceError: If service creation fails
    """
    return AIService(tenant_id=tenant_id, db=db)
