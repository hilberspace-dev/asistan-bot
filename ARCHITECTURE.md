# 🏗️ Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Virtual Receptionist SaaS                │
│                  (Turkish Market - SaaS Platform)           │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Architecture Diagram

```
┌──────────────┐
│   Browser    │
│  (User UI)   │
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Application                    │
│  ┌────────────────────────────────────────────────────┐  │
│  │              main.py (Entry Point)                 │  │
│  │  • Route Registration                              │  │
│  │  • Middleware Setup                                │  │
│  │  • Jinja2 Template Engine                          │  │
│  └────────────────────────────────────────────────────┘  │
│                           │                              │
│         ┌─────────────────┼─────────────────┐           │
│         ▼                 ▼                 ▼           │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐      │
│  │ Dashboard│      │   API    │      │  Health  │      │
│  │   (/)    │      │(/tenants)│      │  Check   │      │
│  └──────────┘      └────┬─────┘      └──────────┘      │
│                          │                              │
└──────────────────────────┼──────────────────────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────┐
         │        app/api/tenants.py           │
         │  ┌────────────────────────────┐     │
         │  │  • POST   /api/tenants/    │     │
         │  │  • GET    /api/tenants/    │     │
         │  │  • GET    /api/tenants/:id │     │
         │  │  • PUT    /api/tenants/:id │     │
         │  │  • DELETE /api/tenants/:id │     │
         │  └────────────────────────────┘     │
         └───────────────┬─────────────────────┘
                         │
                         ▼
         ┌────────────────────────────────────┐
         │     app/core/database.py           │
         │  • SessionLocal Factory            │
         │  • get_db() Dependency             │
         │  • Base (Declarative)              │
         └───────────────┬────────────────────┘
                         │
                         ▼
         ┌────────────────────────────────────┐
         │    app/models/tenant.py            │
         │  ┌──────────────────────────────┐  │
         │  │  Tenant Model:               │  │
         │  │  • id (PK)                   │  │
         │  │  • username (unique)         │  │
         │  │  • password_hash (bcrypt)    │  │
         │  │  • openai_api_key (encrypted)│  │
         │  │  • business_name             │  │
         │  │  • system_prompt             │  │
         │  │  • timestamps                │  │
         │  └──────────────────────────────┘  │
         └───────────────┬────────────────────┘
                         │
                         ▼
         ┌────────────────────────────────────┐
         │          SQLite Database           │
         │     randevu_asistani.db            │
         └────────────────────────────────────┘

         ┌────────────────────────────────────┐
         │    app/core/security.py            │
         │  • EncryptionManager (Fernet)      │
         │  • get_password_hash()             │
         │  • verify_password()               │
         └────────────────────────────────────┘
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layer                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Password Security (bcrypt)                          │
│     ┌─────────────┐         ┌─────────────┐           │
│     │   Plain     │  hash   │   Hashed    │           │
│     │  Password   │────────>│  Password   │           │
│     │  "abc123"   │         │  "$2b$12..."│           │
│     └─────────────┘         └─────────────┘           │
│                                                         │
│  2. API Key Encryption (Fernet)                        │
│     ┌─────────────┐         ┌─────────────┐           │
│     │   Plain     │ encrypt │  Encrypted  │           │
│     │  API Key    │────────>│   API Key   │           │
│     │ "sk-proj..."│         │ "gAAAA..."  │           │
│     └─────────────┘         └─────────────┘           │
│            ▲                                            │
│            │ decrypt                                    │
│            └─────────────────────                       │
│                                                         │
│  3. Encryption Key Management                          │
│     • Stored in .env file                              │
│     • Generated with Fernet.generate_key()             │
│     • Never committed to git                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📦 Module Structure

```
app/
├── core/                    # Core functionality
│   ├── config.py           # Settings & Configuration
│   │   └── Settings (Pydantic BaseSettings)
│   │       • APP_NAME, VERSION
│   │       • DATABASE_URL
│   │       • SECRET_KEY, ENCRYPTION_KEY
│   │
│   ├── database.py         # Database Session Management
│   │   • engine (SQLAlchemy Engine)
│   │   • SessionLocal (Session Factory)
│   │   • Base (Declarative Base)
│   │   • get_db() (Dependency)
│   │   • init_db() (Initialize Tables)
│   │
│   └── security.py         # Security Utilities
│       • EncryptionManager Class
│       │   ├── encrypt(plain_text) -> encrypted
│       │   └── decrypt(encrypted) -> plain_text
│       • get_password_hash(password) -> hash
│       • verify_password(plain, hash) -> bool
│
├── models/                 # Database Models
│   └── tenant.py
│       └── Tenant (SQLAlchemy Model)
│           • id, username, password_hash
│           • business_name, system_prompt
│           • openai_api_key (encrypted)
│           • set_openai_api_key(plain)
│           • get_openai_api_key() -> plain
│           • to_dict()
│
├── api/                    # API Routes
│   └── tenants.py
│       • TenantCreate (Pydantic Schema)
│       • TenantUpdate (Pydantic Schema)
│       • TenantResponse (Pydantic Schema)
│       • POST   /api/tenants/ (create)
│       • GET    /api/tenants/ (list)
│       • GET    /api/tenants/{id} (read)
│       • PUT    /api/tenants/{id} (update)
│       • DELETE /api/tenants/{id} (delete)
│
└── templates/              # Jinja2 Templates
    └── dashboard.html      # Main Dashboard UI
```

## 🔄 Request Flow

### Example: Create Tenant

```
1. Client Request
   POST /api/tenants/
   {
     "username": "ahmet_dis",
     "password": "secret123",
     "openai_api_key": "sk-...",
     "business_name": "Ahmet Diş Kliniği",
     "system_prompt": "Sen bir asistansın..."
   }
   
2. FastAPI Router
   • Route to tenants.create_tenant()
   • Validate with Pydantic (TenantCreate)
   
3. API Handler (app/api/tenants.py)
   • Check username uniqueness
   • Hash password with bcrypt
   • Create Tenant instance
   
4. Model Layer (app/models/tenant.py)
   • tenant.set_openai_api_key()
   • Encrypt API key with Fernet
   
5. Database Layer
   • db.add(tenant)
   • db.commit()
   • db.refresh(tenant)
   
6. Response
   {
     "id": 1,
     "username": "ahmet_dis",
     "business_name": "Ahmet Diş Kliniği",
     "system_prompt": "Sen bir asistansın..."
   }
   (Note: API key NOT included in response)
```

## 🗄️ Database Schema

```sql
CREATE TABLE tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    business_name VARCHAR(255) NOT NULL,
    openai_api_key TEXT NOT NULL,  -- Encrypted
    system_prompt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

CREATE INDEX ix_tenants_username ON tenants(username);
CREATE INDEX ix_tenants_id ON tenants(id);
```

## 🎯 Design Patterns

### 1. Dependency Injection
```python
# Database session injection
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in endpoints
@router.post("/")
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)  # Auto-injected
):
    ...
```

### 2. Repository Pattern
```python
# Model acts as repository
class Tenant(Base):
    def set_openai_api_key(self, plain_key: str):
        # Encapsulates encryption logic
        self.openai_api_key = encryption_manager.encrypt(plain_key)
```

### 3. Singleton Pattern
```python
# Global encryption manager instance
encryption_manager = EncryptionManager()
```

### 4. Settings Pattern
```python
# Centralized configuration
class Settings(BaseSettings):
    APP_NAME: str = "..."
    DATABASE_URL: str = "..."
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 🚀 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web Framework** | FastAPI | High-performance async API |
| **ASGI Server** | Uvicorn | Production ASGI server |
| **ORM** | SQLAlchemy | Database abstraction |
| **Database** | SQLite | Lightweight embedded DB |
| **Templating** | Jinja2 | Server-side rendering |
| **Validation** | Pydantic | Data validation & serialization |
| **Encryption** | Fernet (cryptography) | Symmetric encryption |
| **Password Hashing** | bcrypt (passlib) | Secure password hashing |
| **Environment** | python-dotenv | Config management |

## 📈 Scalability Considerations

### Current Architecture (Phase 1)
- ✅ Single SQLite database
- ✅ Single application instance
- ✅ Suitable for: 100-1000 tenants

### Future Enhancements (Phase 2+)
- [ ] PostgreSQL for production
- [ ] Redis for caching
- [ ] Load balancer (nginx)
- [ ] Multiple app instances
- [ ] Database read replicas
- [ ] Message queue (RabbitMQ/Celery)
- [ ] Microservices architecture

## 🔍 Security Best Practices Implemented

1. ✅ **Never store plain passwords** - bcrypt hashing
2. ✅ **Never store plain API keys** - Fernet encryption
3. ✅ **Environment-based secrets** - .env files
4. ✅ **Input validation** - Pydantic schemas
5. ✅ **SQL injection protection** - SQLAlchemy ORM
6. ✅ **Secure password requirements** - min 6 chars
7. ✅ **Proper error messages** - Turkish, no sensitive info

## 📊 Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Create Tenant | O(1) | + bcrypt hashing (slow by design) |
| List Tenants | O(n) | Paginated with skip/limit |
| Get Tenant | O(1) | Indexed by ID |
| Update Tenant | O(1) | + optional bcrypt/encrypt |
| Delete Tenant | O(1) | Direct by ID |
| Decrypt API Key | O(1) | Fernet symmetric decrypt |

---

**Architecture Status**: Production Ready ✅  
**Security Level**: High 🔒  
**Scalability**: Medium (suitable for MVP) 📈  
**Documentation**: Comprehensive 📚
