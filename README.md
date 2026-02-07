# 🤖 Virtual Receptionist SaaS

Türk pazarı için yapay zeka destekli sanal resepsiyon sistemi.

## 📋 Özellikler

- ✅ **Multi-tenant Mimari**: Her işletme için ayrı hesap ve yapılandırma
- 🔒 **Güvenli API Key Saklama**: OpenAI API anahtarları Fernet şifreleme ile korunur
- ⚙️ **Özelleştirilebilir Bot**: Her işletme kendi sistem talimatlarını belirleyebilir
- 🚀 **FastAPI Backend**: Yüksek performanslı ve modern Python framework
- 💾 **SQLite Veritabanı**: Hafif ve kolay yönetilebilir
- 🎨 **Admin Dashboard**: TailwindCSS ile modern, Türkçe yönetim paneli
- 🔐 **Session Authentication**: Güvenli oturum yönetimi
- 📱 **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- 🤖 **AI Service**: OpenAI GPT entegrasyonu, otomatik Türkçe zorlama
- 💬 **Chat API**: Standard ve streaming chat completions

## 🏗️ Proje Yapısı

```
randevu-asistani/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Uygulama yapılandırması
│   │   ├── database.py        # Veritabanı bağlantı yönetimi
│   │   └── security.py        # Şifreleme ve güvenlik fonksiyonları
│   ├── models/
│   │   ├── __init__.py
│   │   └── tenant.py          # Müşteri (Tenant) modeli
│   ├── api/
│   │   ├── __init__.py
│   │   └── tenants.py         # Müşteri API endpoints
│   └── templates/
│       └── dashboard.html     # Ana kontrol paneli
├── main.py                    # FastAPI uygulama giriş noktası
├── database.py                # Veritabanı yardımcı scriptleri
├── requirements.txt           # Python bağımlılıkları
├── .env.example              # Örnek environment dosyası
└── README.md                 # Bu dosya
```

## 🚀 Kurulum

### 1. Sanal Ortam Oluşturun

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Environment Dosyasını Yapılandırın

```bash
# .env.example dosyasını kopyalayın
copy .env.example .env

# Şifreleme anahtarı oluşturun
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Oluşturulan anahtarı `.env` dosyasındaki `ENCRYPTION_KEY` değişkenine yapıştırın.

### 4. Veritabanını Başlatın

```bash
python database.py
```

### 5. Demo Kullanıcı Oluşturun

```bash
python create_demo_user.py
```

Bu komut test için bir demo kullanıcı oluşturur:
- **Username**: demo
- **Password**: demo123
- **Business**: Demo Diş Kliniği

### 6. Sunucuyu Başlatın

```bash
python main.py
```

Uygulama şu adreste çalışacaktır: http://localhost:8000

## 📚 API Dokümantasyonu

FastAPI otomatik olarak interaktif API dokümantasyonu oluşturur:

- **Ana Sayfa**: http://localhost:8000
- **Yönetim Paneli Girişi**: http://localhost:8000/giris
- **Dashboard Panel**: http://localhost:8000/panel
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Admin Panel

### Giriş Yapma

1. Tarayıcınızda açın: http://localhost:8000/giris
2. Demo kullanıcı ile giriş yapın:
   - **Kullanıcı Adı**: demo
   - **Şifre**: demo123
3. "Giriş Yap" butonuna tıklayın

### Dashboard Panel

Giriş yaptıktan sonra yönetim paneline yönlendirilirsiniz:

- ✅ **OpenAI API Anahtarı**: Güvenli şekilde güncelleyin
- ✅ **Bot Talimatları**: Sistem prompt'unu düzenleyin
- ✅ **İşletme Adı**: İşletme adınızı değiştirin
- ✅ **Başarı Bildirimleri**: Değişiklikler kaydedildiğinde bildirim alın

Detaylı kullanım için: [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md)

## 🤖 AI Service (OpenAI Integration)

### Chat Completions

Yapay zeka asistanı ile etkileşim kurun:

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "user_message": "Merhaba! Randevu almak istiyorum.",
    "model": "gpt-4o-mini"
  }'
```

**Özellikler:**
- ✅ **Otomatik Türkçe**: Tüm cevaplar Türkçe
- ✅ **Dinamik Yapılandırma**: Her tenant kendi API key'i kullanır
- ✅ **Streaming Desteği**: Gerçek zamanlı yanıtlar
- ✅ **Konuşma Geçmişi**: Bağlam korumalı diyaloglar

### Python Kullanımı

```python
from app.core.ai_service import create_ai_service
from app.core.database import SessionLocal

db = SessionLocal()
ai_service = create_ai_service(tenant_id=1, db=db)

response = ai_service.chat_completion(
    user_message="Merhaba! Nasılsınız?"
)
print(response)
```

### Test Et

```bash
python test_ai_service.py
```

Detaylı kullanım için: [AI_SERVICE_GUIDE.md](AI_SERVICE_GUIDE.md)

## 🔌 API Endpoints

### Müşteri İşlemleri

#### Yeni Müşteri Oluştur
```bash
POST /api/tenants/

{
  "username": "ahmet_dis_klinigi",
  "password": "guvenli_sifre123",
  "business_name": "Ahmet Diş Kliniği",
  "openai_api_key": "sk-...",
  "system_prompt": "Sen Ahmet Diş Kliniği'nin sanal resepsiyonistisin..."
}
```

#### Tüm Müşterileri Listele
```bash
GET /api/tenants/
```

#### Müşteri Detaylarını Getir
```bash
GET /api/tenants/{tenant_id}
```

#### Müşteri Bilgilerini Güncelle
```bash
PUT /api/tenants/{tenant_id}

{
  "business_name": "Yeni İşletme Adı",
  "system_prompt": "Güncellenmiş sistem talimatları..."
}
```

#### Müşteri Sil
```bash
DELETE /api/tenants/{tenant_id}
```

## 🔒 Güvenlik

### API Key Şifreleme

OpenAI API anahtarları `cryptography` kütüphanesinin Fernet simetrik şifreleme algoritması ile korunur:

```python
from app.models.tenant import Tenant

tenant = Tenant(...)
tenant.set_openai_api_key("sk-...")  # Otomatik şifrelenir

# Kullanım sırasında
api_key = tenant.get_openai_api_key()  # Otomatik deşifre edilir
```

### Parola Hashleme

Kullanıcı parolaları `bcrypt` algoritması ile hashlenmiştir:

```python
from app.core.security import get_password_hash, verify_password

hashed = get_password_hash("sifre123")
is_valid = verify_password("sifre123", hashed)
```

## 🗃️ Veritabanı Modeli

### Tenant (Müşteri)

| Alan | Tip | Açıklama |
|------|-----|----------|
| id | Integer | Birincil anahtar |
| username | String | Benzersiz kullanıcı adı |
| password_hash | String | Hashlenmiş parola |
| business_name | String | İşletme adı |
| openai_api_key | Text | Şifreli API anahtarı |
| system_prompt | Text | Bot talimatları |
| created_at | DateTime | Oluşturulma zamanı |
| updated_at | DateTime | Güncellenme zamanı |

## 🛠️ Geliştirme

### Veritabanını Sıfırlama

```bash
python database.py reset
```

### Test Müşteri Oluşturma

```bash
curl -X POST "http://localhost:8000/api/tenants/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_klinik",
    "password": "test123456",
    "business_name": "Test Kliniği",
    "openai_api_key": "sk-test-key",
    "system_prompt": "Sen bir test resepsiyonistisin."
  }'
```

## 📝 Sonraki Adımlar

- [x] Admin paneli ✅
- [x] OpenAI GPT entegrasyonu ✅
- [x] Türkçe chat completions ✅
- [ ] WhatsApp/Telegram entegrasyonu
- [ ] Randevu yönetim sistemi
- [ ] Müşteri istatistikleri ve raporlama
- [ ] Ses asistan entegrasyonu
- [ ] WebSocket real-time chat

## 📄 Lisans

Bu proje özel bir projedir.

## 👨‍💻 Geliştirici

Senior Python Backend Engineer tarafından geliştirilmiştir.

---

🇹🇷 **Türk Pazarı için Özel Olarak Geliştirilmiştir**
