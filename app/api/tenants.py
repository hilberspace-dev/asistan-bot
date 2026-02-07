"""
Tenant API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.models.tenant import Tenant


router = APIRouter()


# Pydantic schemas
class TenantCreate(BaseModel):
    """Schema for creating a new tenant"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6)
    business_name: str = Field(..., min_length=1, max_length=255)
    openai_api_key: str = Field(..., min_length=20)
    system_prompt: str = Field(
        default="Sen bir sanal resepsiyonistsin. Müşterilere profesyonel ve nazik bir şekilde yardımcı oluyorsun.",
        min_length=10
    )


class TenantUpdate(BaseModel):
    """Schema for updating tenant"""
    business_name: str | None = Field(None, min_length=1, max_length=255)
    openai_api_key: str | None = Field(None, min_length=20)
    system_prompt: str | None = Field(None, min_length=10)
    password: str | None = Field(None, min_length=6)


class TenantResponse(BaseModel):
    """Schema for tenant response"""
    id: int
    username: str
    business_name: str
    system_prompt: str
    
    class Config:
        from_attributes = True


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    """
    Create a new tenant (Müşteri)
    
    Args:
        tenant_data: Tenant creation data
        db: Database session
        
    Returns:
        Created tenant
    """
    # Check if username already exists
    existing_tenant = db.query(Tenant).filter(Tenant.username == tenant_data.username).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kullanıcı adı zaten kullanılıyor"
        )
    
    # Create new tenant
    new_tenant = Tenant(
        username=tenant_data.username,
        password_hash=get_password_hash(tenant_data.password),
        business_name=tenant_data.business_name,
        system_prompt=tenant_data.system_prompt
    )
    
    # Encrypt and set API key
    new_tenant.set_openai_api_key(tenant_data.openai_api_key)
    
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    
    return new_tenant


@router.get("/", response_model=List[TenantResponse])
async def list_tenants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all tenants
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of tenants
    """
    tenants = db.query(Tenant).offset(skip).limit(limit).all()
    return tenants


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get a specific tenant by ID
    
    Args:
        tenant_id: Tenant ID
        db: Database session
        
    Returns:
        Tenant details
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Müşteri bulunamadı"
        )
    
    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db)
):
    """
    Update tenant information
    
    Args:
        tenant_id: Tenant ID
        tenant_data: Update data
        db: Database session
        
    Returns:
        Updated tenant
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Müşteri bulunamadı"
        )
    
    # Update fields if provided
    if tenant_data.business_name:
        tenant.business_name = tenant_data.business_name
    
    if tenant_data.system_prompt:
        tenant.system_prompt = tenant_data.system_prompt
    
    if tenant_data.openai_api_key:
        tenant.set_openai_api_key(tenant_data.openai_api_key)
    
    if tenant_data.password:
        tenant.password_hash = get_password_hash(tenant_data.password)
    
    db.commit()
    db.refresh(tenant)
    
    return tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """
    Delete a tenant
    
    Args:
        tenant_id: Tenant ID
        db: Database session
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Müşteri bulunamadı"
        )
    
    db.delete(tenant)
    db.commit()
    
    return None
