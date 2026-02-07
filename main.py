import os
import time
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
import openai  # OpenAI kütüphanesini ekledik

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- AYARLAR ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
DATABASE_URL = "sqlite:///./randevu_v2.db"

# --- VERİTABANI MODELİ ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    business_name = Column(String)
    openai_api_key = Column(String, nullable=True)
    system_prompt = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Gelen mesaj formatı
class ChatMessage(BaseModel):
    message: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- BAŞLANGIÇ KONTROLÜ ---
@app.on_event("startup")
def startup_db_check():
    db = SessionLocal()
    try:
        existing_user = db.query(Tenant).filter(Tenant.username == "demo").first()
        if not existing_user:
            demo_user = Tenant(
                username="demo",
                password="123",
                business_name="Demo Klinik",
                system_prompt="Sen yardımsever bir asistansın."
            )
            db.add(demo_user)
            db.commit()
            print("--- DEMO KULLANICI HAZIR ---")
    finally:
        db.close()

# --- SAYFALAR ---

@app.get("/giris", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("giris.html", {"request": request})

@app.post("/giris")
async def login_submit(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Tenant).filter(Tenant.username == username).first()
    
    # Check if password is plain text (for backwards compatibility) or hashed
    if not user:
        return templates.TemplateResponse("giris.html", {"request": request, "error": "Kullanıcı bulunamadı!"})
    
    # Try plain text first (backwards compatibility), then try bcrypt verification
    password_valid = (user.password == password) or pwd_context.verify(password, user.password)
    
    if not password_valid:
        return templates.TemplateResponse("giris.html", {"request": request, "error": "Hatalı Şifre!"})
    
    response = RedirectResponse(url="/panel", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))
    return response

@app.get("/panel", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id: return RedirectResponse(url="/giris")
    
    user = db.query(Tenant).filter(Tenant.id == int(user_id)).first()
    return templates.TemplateResponse("panel.html", {
        "request": request, 
        "username": user.username,
        "business_name": user.business_name,
        "api_key": user.openai_api_key or "",
        "system_prompt": user.system_prompt or "",
        "success": None,
        "error": None
    })

@app.post("/ayarlari-kaydet")
async def save_settings(
    request: Request, 
    openai_key: str = Form(...), 
    bot_prompt: str = Form(...),
    business_name: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if not user_id: return RedirectResponse(url="/giris")

    user = db.query(Tenant).filter(Tenant.id == int(user_id)).first()
    user.openai_api_key = openai_key
    user.system_prompt = bot_prompt
    user.business_name = business_name
    db.commit()
    
    return templates.TemplateResponse("panel.html", {
        "request": request,
        "username": user.username,
        "business_name": business_name,
        "api_key": openai_key,
        "system_prompt": bot_prompt,
        "success": "✅ Ayarlar ve Anahtar Güvenle Kaydedildi!"
    })

# --- YENİ EKLENEN KISIM: MÜŞTERİ CHAT EKRANI ---
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, db: Session = Depends(get_db)):
    # Safer query - look for demo user by username
    user = db.query(Tenant).filter(Tenant.username == "demo").first()
    
    # Fallback if DB is empty
    b_name = user.business_name if user else "Sanal Asistan"
    
    return templates.TemplateResponse("chat.html", {"request": request, "business_name": b_name})

# --- YENİ EKLENEN KISIM: YAPAY ZEKA API (BEYİN) ---
@app.post("/chat-api")
async def chat_endpoint(chat_data: ChatMessage, db: Session = Depends(get_db)):
    # 1. Veritabanından müşterinin kaydettiği Key'i bul (demo user)
    user = db.query(Tenant).filter(Tenant.username == "demo").first()
    
    if not user or not user.openai_api_key:
        return JSONResponse(content={"error": "Klinik henüz API anahtarı girmemiş. Lütfen yöneticiye bildirin."}, status_code=400)

    # SIMULATION MODE: API key "TEST" ise gerçek OpenAI çağrısı yapma
    if user.openai_api_key.upper() == "TEST":
        # Network delay simülasyonu (1 saniye bekle)
        time.sleep(1)
        
        # Simülasyon yanıtı döndür
        return {"reply": "Sistem BAŞARIYLA çalışıyor! Paran cebinde kaldı. Mesajın sunucuya ulaştı ve bu yapay cevap döndü. 🚀"}
    
    # GERÇEK MOD: OpenAI'ya bağlan
    try:
        # 2. Müşterinin kendi anahtarını kullanarak OpenAI'ya bağlan
        client = openai.OpenAI(api_key=user.openai_api_key)
        
        # 3. Müşterinin yazdığı talimatla (prompt) cevap ver
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": user.system_prompt},
                {"role": "user", "content": chat_data.message}
            ]
        )
        
        bot_reply = response.choices[0].message.content
        return {"reply": bot_reply}
        
    except Exception as e:
        return JSONResponse(content={"error": f"OpenAI Hatası: {str(e)}"}, status_code=500)

@app.post("/update-credentials")
async def update_credentials(
    request: Request,
    current_password: str = Form(...),
    new_username: str = Form(None),
    new_password: str = Form(None),
    new_password_confirm: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update user credentials (username and/or password)"""
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/giris")
    
    user = db.query(Tenant).filter(Tenant.id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/giris")
    
    # 1. Verify current password
    password_valid = (user.password == current_password) or pwd_context.verify(current_password, user.password)
    
    if not password_valid:
        return templates.TemplateResponse("panel.html", {
            "request": request,
            "username": user.username,
            "business_name": user.business_name,
            "api_key": user.openai_api_key or "",
            "system_prompt": user.system_prompt or "",
            "error": "❌ Mevcut şifre hatalı!"
        })
    
    # 2. Update username if provided
    if new_username and new_username.strip():
        # Check if username already exists
        existing = db.query(Tenant).filter(Tenant.username == new_username, Tenant.id != user.id).first()
        if existing:
            return templates.TemplateResponse("panel.html", {
                "request": request,
                "username": user.username,
                "business_name": user.business_name,
                "api_key": user.openai_api_key or "",
                "system_prompt": user.system_prompt or "",
                "error": "❌ Bu kullanıcı adı zaten kullanılıyor!"
            })
        user.username = new_username.strip()
    
    # 3. Update password if provided (HASH IT!)
    if new_password and new_password.strip():
        # Validate password confirmation
        if new_password != new_password_confirm:
            return templates.TemplateResponse("panel.html", {
                "request": request,
                "username": user.username,
                "business_name": user.business_name,
                "api_key": user.openai_api_key or "",
                "system_prompt": user.system_prompt or "",
                "error": "❌ Şifreler uyuşmuyor! Lütfen aynı şifreyi iki kez girin."
            })
        
        user.password = pwd_context.hash(new_password)
    
    # 4. Commit changes
    db.commit()
    
    # 5. Redirect back with success message
    return templates.TemplateResponse("panel.html", {
        "request": request,
        "username": user.username,
        "business_name": user.business_name,
        "api_key": user.openai_api_key or "",
        "system_prompt": user.system_prompt or "",
        "success": "✅ Hesap bilgileriniz başarıyla güncellendi!"
    })


@app.get("/")
def root():
    return RedirectResponse("/giris")