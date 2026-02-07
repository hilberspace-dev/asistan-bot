"""
Chat API Routes
Endpoints for interacting with the AI assistant
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from app.core.database import get_db
from app.core.ai_service import create_ai_service, AIServiceError


router = APIRouter()


# Pydantic schemas
class Message(BaseModel):
    """Single message in conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request"""
    tenant_id: int = Field(..., description="Tenant ID")
    user_message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    conversation_history: Optional[List[Message]] = Field(
        default=None,
        description="Previous conversation messages"
    )
    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Response randomness")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens in response")
    stream: bool = Field(default=False, description="Enable streaming response")


class ChatResponse(BaseModel):
    """Chat completion response"""
    tenant_id: int
    business_name: str
    user_message: str
    assistant_message: str
    model: str
    success: bool


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: str


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a chat completion using the tenant's AI assistant
    
    Args:
        request: Chat request with tenant_id and message
        db: Database session
        
    Returns:
        Assistant's response
        
    Raises:
        HTTPException: If tenant not found or API error
    """
    try:
        # Create AI service for tenant
        ai_service = create_ai_service(tenant_id=request.tenant_id, db=db)
        
        # Convert conversation history to dict format
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Get chat completion
        assistant_message = ai_service.chat_completion(
            user_message=request.user_message,
            conversation_history=history,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            tenant_id=request.tenant_id,
            business_name=ai_service.tenant.business_name,
            user_message=request.user_message,
            assistant_message=assistant_message,
            model=request.model,
            success=True
        )
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/chat/stream")
async def chat_completion_stream(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a streaming chat completion
    
    Args:
        request: Chat request with tenant_id and message
        db: Database session
        
    Returns:
        Streaming response with assistant's message
        
    Raises:
        HTTPException: If tenant not found or API error
    """
    try:
        # Create AI service for tenant
        ai_service = create_ai_service(tenant_id=request.tenant_id, db=db)
        
        # Convert conversation history to dict format
        history = None
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Get streaming generator
        stream_generator = ai_service.chat_completion_stream(
            user_message=request.user_message,
            conversation_history=history,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return StreamingResponse(
            stream_generator,
            media_type="text/plain",
            headers={
                "X-Tenant-ID": str(request.tenant_id),
                "X-Model": request.model
            }
        )
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tenant/{tenant_id}/models")
async def get_available_models(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Get available OpenAI models for a tenant
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        List of available models
    """
    try:
        ai_service = create_ai_service(tenant_id=tenant_id, db=db)
        models = ai_service.get_available_models()
        
        return {
            "tenant_id": tenant_id,
            "business_name": ai_service.tenant.business_name,
            "available_models": models
        }
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tenant/{tenant_id}/validate")
async def validate_api_key(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Validate tenant's OpenAI API key
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        Validation result
    """
    try:
        ai_service = create_ai_service(tenant_id=tenant_id, db=db)
        is_valid = ai_service.validate_api_key()
        
        return {
            "tenant_id": tenant_id,
            "business_name": ai_service.tenant.business_name,
            "api_key_valid": is_valid,
            "message": "API key is valid and working" if is_valid else "API key validation failed"
        }
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tenant/{tenant_id}/info")
async def get_tenant_ai_info(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Get tenant's AI configuration info
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        Tenant AI configuration details
    """
    try:
        ai_service = create_ai_service(tenant_id=tenant_id, db=db)
        info = ai_service.get_tenant_info()
        
        return {
            "success": True,
            "tenant_info": info,
            "system_prompt_preview": ai_service.system_prompt[:200] + "..." if len(ai_service.system_prompt) > 200 else ai_service.system_prompt
        }
        
    except AIServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
