"""
Authentication API Routes
Login, Dashboard Panel, and Session Management
"""
import os
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash
from app.models.tenant import Tenant


router = APIRouter()

# Calculate absolute path to templates directory (ROOT level)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates_path = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=templates_path)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[Tenant]:
    """
    Get currently logged in user from session
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Tenant object if logged in, None otherwise
    """
    tenant_id = request.session.get("tenant_id")
    if not tenant_id:
        return None
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    return tenant


def require_auth(request: Request, db: Session = Depends(get_db)) -> Tenant:
    """
    Require authentication, redirect to login if not authenticated
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Tenant object
        
    Raises:
        RedirectResponse if not authenticated
    """
    tenant = get_current_user(request, db)
    if not tenant:
        return RedirectResponse(url="/giris", status_code=302)
    return tenant


@router.get("/giris", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Display login page (GET)
    
    Args:
        request: FastAPI request object
        
    Returns:
        HTML login page
    """
    # If already logged in, redirect to panel
    if request.session.get("tenant_id"):
        return RedirectResponse(url="/panel", status_code=302)
    
    return templates.TemplateResponse(
        "giris.html",
        {
            "request": request,
            "error": None,
            "username": None
        }
    )


@router.post("/giris", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    remember: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Handle login form submission (POST)
    
    Args:
        request: FastAPI request object
        username: Username from form
        password: Password from form
        remember: Remember me checkbox
        db: Database session
        
    Returns:
        Redirect to panel on success, login page with error on failure
    """
    # Find tenant by username
    tenant = db.query(Tenant).filter(Tenant.username == username).first()
    
    # Verify credentials
    if not tenant or not verify_password(password, tenant.password_hash):
        return templates.TemplateResponse(
            "giris.html",
            {
                "request": request,
                "error": "Kullanıcı adı veya şifre hatalı",
                "username": username
            },
            status_code=401
        )
    
    # Create session
    request.session["tenant_id"] = tenant.id
    request.session["username"] = tenant.username
    request.session["business_name"] = tenant.business_name
    
    # Set session expiry if remember me is checked
    if remember:
        request.session["permanent"] = True
    
    # Redirect to panel
    return RedirectResponse(url="/panel", status_code=302)


@router.get("/panel", response_class=HTMLResponse)
async def panel_page(request: Request, db: Session = Depends(get_db)):
    """
    Display dashboard panel (GET)
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        HTML panel page or redirect to login
    """
    # Check authentication
    tenant = get_current_user(request, db)
    if not tenant:
        return RedirectResponse(url="/giris", status_code=302)
    
    return templates.TemplateResponse(
        "panel.html",
        {
            "request": request,
            "tenant_id": tenant.id,
            "username": tenant.username,
            "business_name": tenant.business_name,
            "system_prompt": tenant.system_prompt,
            "api_key": tenant.get_openai_api_key() if tenant.openai_api_key else None,
            "success": None
        }
    )


@router.post("/panel", response_class=HTMLResponse)
async def panel_submit(
    request: Request,
    api_key: Optional[str] = Form(None),
    system_prompt: str = Form(...),
    business_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handle panel form submission (POST)
    Update tenant settings
    
    Args:
        request: FastAPI request object
        api_key: OpenAI API key (optional, only update if provided and not masked)
        system_prompt: Bot instructions
        business_name: Business name
        db: Database session
        
    Returns:
        Panel page with success message or redirect to login
    """
    # Check authentication
    tenant = get_current_user(request, db)
    if not tenant:
        return RedirectResponse(url="/giris", status_code=302)
    
    # Update business name
    tenant.business_name = business_name
    
    # Update system prompt
    tenant.system_prompt = system_prompt
    
    # Update API key only if it's not masked (not all bullets)
    if api_key and not all(c == '•' for c in api_key.strip()):
        if api_key.strip():  # Only update if not empty
            tenant.set_openai_api_key(api_key)
    
    # Save to database
    db.commit()
    db.refresh(tenant)
    
    # Update session with new business name
    request.session["business_name"] = tenant.business_name
    
    return templates.TemplateResponse(
        "panel.html",
        {
            "request": request,
            "tenant_id": tenant.id,
            "username": tenant.username,
            "business_name": tenant.business_name,
            "system_prompt": tenant.system_prompt,
            "api_key": tenant.get_openai_api_key() if tenant.openai_api_key else None,
            "success": "Ayarlarınız başarıyla kaydedildi!"
        }
    )


@router.get("/cikis")
async def logout(request: Request):
    """
    Logout user and clear session
    
    Args:
        request: FastAPI request object
        
    Returns:
        Redirect to login page
    """
    # Clear session
    request.session.clear()
    
    # Redirect to login
    return RedirectResponse(url="/giris", status_code=302)
