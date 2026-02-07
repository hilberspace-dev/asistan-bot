# 🎨 Admin Panel Kullanım Kılavuzu

## 📋 İçindekiler

1. [Giriş](#giriş)
2. [Login Sayfası](#login-sayfası)
3. [Yönetim Paneli](#yönetim-paneli)
4. [Özellikler](#özellikler)
5. [Güvenlik](#güvenlik)

---

## 🚀 Giriş

Admin Panel, Virtual Receptionist SaaS platformunda müşterilerin (tenant) kendi sanal resepsiyon botlarını yönetebilecekleri modern ve kullanıcı dostu bir arayüzdür.

### Teknolojiler

- **Frontend**: HTML5, TailwindCSS (CDN)
- **Template Engine**: Jinja2
- **Backend**: FastAPI + Session Management
- **Güvenlik**: bcrypt password hashing, Fernet encryption

---

## 🔐 Login Sayfası

### URL
```
http://localhost:8000/giris
```

### Özellikler

#### 1. **Modern Gradient Tasarım**
- Mor-indigo gradient arkaplan
- Responsive tasarım (mobil uyumlu)
- Smooth animasyonlar

#### 2. **Form Alanları**
- ✅ **Kullanıcı Adı**: SVG icon ile görsel destekli
- ✅ **Şifre**: Güvenli password input
- ✅ **Beni Hatırla**: 30 gün oturum süresi

#### 3. **Hata Yönetimi**
- Yanlış kullanıcı adı/şifre için Türkçe hata mesajı
- Kırmızı border-left ile görsel vurgu
- Kullanıcı adı form'da kalır (tekrar yazılmaz)

#### 4. **UX İyileştirmeleri**
- Auto-focus kullanıcı adı alanında
- Enter tuşu ile giriş
- Hover efektleri
- Loading states

### Demo Kullanıcı

```bash
# Demo kullanıcı oluştur
python create_demo_user.py

# Login bilgileri
Username: demo
Password: demo123
```

### Ekran Görüntüsü Özellikleri

```
┌─────────────────────────────────────────┐
│            🤖 Logo                      │
│      Yönetim Paneli                     │
│   Sanal Resepsiyon Asistanı             │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │       Giriş Yap                   │ │
│  │                                   │ │
│  │  👤 Kullanıcı Adı                 │ │
│  │  [________________]               │ │
│  │                                   │ │
│  │  🔒 Şifre                         │ │
│  │  [________________]               │ │
│  │                                   │ │
│  │  ☑ Beni Hatırla                  │ │
│  │                                   │ │
│  │  [    Giriş Yap    ]             │ │
│  └───────────────────────────────────┘ │
│                                         │
│      ← Ana Sayfaya Dön                 │
└─────────────────────────────────────────┘
```

---

## 🎛️ Yönetim Paneli

### URL
```
http://localhost:8000/panel
```

### Üst Navigasyon

```
┌────────────────────────────────────────────────────────┐
│ 🤖 Yönetim Paneli        Demo Diş Kliniği    [Çıkış]  │
│    Virtual Receptionist        @demo                   │
└────────────────────────────────────────────────────────┘
```

Özellikler:
- Logo ve uygulama adı
- İşletme adı ve kullanıcı adı gösterimi
- Çıkış butonu (oturumu sonlandırır)

### Hoşgeldin Bölümü

```
┌────────────────────────────────────────────────────┐
│  Hoşgeldiniz, Demo Diş Kliniği! 👋                │
│  Sanal resepsiyon asistanınızı buradan yönetin    │
└────────────────────────────────────────────────────┘
```

### Başarı Bildirimi

Ayarlar kaydedildiğinde:
```
┌────────────────────────────────────────────────────┐
│  ✅ Başarılı!                             [X]     │
│  Ayarlarınız başarıyla kaydedildi!                │
└────────────────────────────────────────────────────┘
```

- 5 saniye sonra otomatik kaybolur
- Manuel kapatma butonu
- Fade-out animasyonu

### Yapay Zeka Ayarları Formu

#### 1. OpenAI API Anahtarı

```
┌────────────────────────────────────────────┐
│ 🔑 OpenAI API Anahtarı                     │
│ [••••••••••••••••••••] 👁️                  │
│ 🔒 API anahtarınız güvenli bir şekilde    │
│    şifrelenerek saklanır.                  │
└────────────────────────────────────────────┘
```

Özellikler:
- Password input (masked)
- Göz icon'u ile göster/gizle
- Fernet encryption ile güvenli saklama
- Boş bırakılırsa değiştirilmez

#### 2. Bot Talimatları

```
┌────────────────────────────────────────────┐
│ Bot Talimatları                            │
│ ┌────────────────────────────────────────┐ │
│ │ Sen Demo Diş Kliniği'nin sanal        │ │
│ │ resepsiyonistisin.                     │ │
│ │                                        │ │
│ │ Görevlerin:                            │ │
│ │ - Randevu almak...                     │ │
│ └────────────────────────────────────────┘ │
│ 💡 Botunuza özel talimatlar verin         │
└────────────────────────────────────────────┘
```

Özellikler:
- 8 satır textarea
- Placeholder ile örnek
- Zorunlu alan
- Resize disabled

#### 3. İşletme Adı

```
┌────────────────────────────────────────────┐
│ 🏢 İşletme Adı                             │
│ [Demo Diş Kliniği___________________]     │
└────────────────────────────────────────────┘
```

#### 4. Kaydet Butonu

```
┌────────────────────────────────────────────┐
│ ⚡ Değişiklikler otomatik     [Ayarları   │
│    kaydedilir                  Kaydet]    │
└────────────────────────────────────────────┘
```

Özellikler:
- Gradient arka plan (mor-indigo)
- Download icon
- Hover scale efekti
- Shadow efektleri

### Bilgi Kartları

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ ⚡ Durum    │  │ ✅ API      │  │ 🕐 Son     │
│             │  │   Bağlantısı│  │   Güncelleme│
│   Aktif     │  │   Bağlı     │  │   Şimdi     │
└─────────────┘  └─────────────┘  └─────────────┘
```

Özellikler:
- 3 kolonlu responsive grid
- Renkli sol border (mor, yeşil, mavi)
- Icon'lu tasarım
- Gerçek zamanlı durumlar

---

## 🎨 Özellikler

### 1. **Tam Türkçe Dil Desteği**

Tüm arayüz Türkçe:
- ✅ Sayfa başlıkları
- ✅ Form etiketleri
- ✅ Placeholder metinler
- ✅ Buton metinleri
- ✅ Hata mesajları
- ✅ Bildirimler

### 2. **Modern UI/UX**

- **TailwindCSS**: Utility-first CSS framework
- **Gradient Backgrounds**: Mor-indigo tema
- **Animasyonlar**: 
  - Fade-in (sayfa yükleme)
  - Slide-in (içerik kartları)
  - Hover efektleri
  - Scale transformations
- **Responsive**: Tüm cihazlarda uyumlu
- **Icons**: SVG inline icons (bağımlılık yok)

### 3. **Güvenlik**

#### Session Management
```python
# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=86400 * 30  # 30 days
)
```

#### Password Protection
```python
# Login'de şifre doğrulama
if not verify_password(password, tenant.password_hash):
    return error_page
```

#### API Key Masking
```python
# Panel'de API key gösterimi
value="{% if api_key %}{{ '•' * 20 }}{% endif %}"
```

### 4. **Form Validation**

- **Required fields**: `required` attribute
- **Type validation**: Password, text inputs
- **Backend validation**: Pydantic schemas
- **Error handling**: Türkçe hata mesajları

### 5. **Session Features**

```python
# Login sonrası session
request.session["tenant_id"] = tenant.id
request.session["username"] = tenant.username
request.session["business_name"] = tenant.business_name

# Beni hatırla
if remember:
    request.session["permanent"] = True
```

### 6. **Interactive Elements**

#### API Key Toggle
```javascript
function toggleApiKey() {
    // Password ↔ Text
    input.type = input.type === 'password' ? 'text' : 'password';
    // Icon değiştir (göz / çizgili göz)
}
```

#### Auto-hide Notification
```javascript
// 5 saniye sonra otomatik gizle
setTimeout(() => {
    notification.style.opacity = '0';
    // Fade-out animasyonu
}, 5000);
```

---

## 🔐 Güvenlik

### 1. **Authentication Flow**

```
1. Kullanıcı /giris sayfasına gider
2. Username + Password girer
3. Backend verify_password() ile kontrol eder
4. Session oluşturulur
5. /panel sayfasına yönlendirilir
6. Her istekte session kontrol edilir
7. Çıkış yapınca session temizlenir
```

### 2. **Session Protection**

```python
def require_auth(request: Request):
    tenant = get_current_user(request)
    if not tenant:
        return RedirectResponse(url="/giris")
    return tenant
```

### 3. **Password Security**

- **bcrypt hashing**: Yavaş ve güvenli
- **Salt**: Otomatik unique salt
- **Cost factor**: 12 rounds (varsayılan)

### 4. **API Key Security**

- **Fernet encryption**: Simetrik şifreleme
- **Masked display**: Panel'de `••••••` gösterim
- **Conditional update**: Sadece yeni key girilirse güncelle

### 5. **CSRF Protection**

- Session middleware otomatik CSRF token yönetimi
- Form POST istekleri korunur

---

## 📊 Endpoint Yapısı

### Authentication Endpoints

```python
# GET /giris - Login sayfası
@router.get("/giris")
async def login_page(request: Request)

# POST /giris - Login form submit
@router.post("/giris")
async def login_submit(
    username: str, 
    password: str, 
    remember: Optional[str]
)

# GET /panel - Dashboard panel
@router.get("/panel")
async def panel_page(request: Request)

# POST /panel - Settings update
@router.post("/panel")
async def panel_submit(
    api_key: str,
    system_prompt: str,
    business_name: str
)

# GET /cikis - Logout
@router.get("/cikis")
async def logout(request: Request)
```

---

## 🧪 Test Senaryoları

### 1. Login Testi

```bash
# Demo user oluştur
python create_demo_user.py

# Server başlat
python main.py

# Tarayıcıda aç
http://localhost:8000/giris

# Login yap
Username: demo
Password: demo123
```

### 2. Panel Testi

```
1. ✅ Başarılı login sonrası panel açılır
2. ✅ İşletme adı ve kullanıcı adı görünür
3. ✅ Mevcut ayarlar form'da dolu gelir
4. ✅ API key masked gösterilir
5. ✅ Ayarları değiştir ve kaydet
6. ✅ Başarı mesajı görünür
7. ✅ 5 saniye sonra otomatik kaybolur
```

### 3. Güvenlik Testi

```
1. ✅ /panel'e direkt gitmek /giris'e yönlendirir
2. ✅ Yanlış şifre hata mesajı verir
3. ✅ Session olmadan panel erişilemez
4. ✅ Çıkış sonrası tekrar giriş gerekir
```

---

## 💡 Kullanım İpuçları

### 1. **API Key Güncelleme**

- Mevcut key'i görmek için göz icon'una tıklayın
- Yeni key girmek için input'u temizleyin
- Boş bırakırsanız eski key korunur
- `••••••` görünüyorsa değiştirilmez

### 2. **System Prompt Yazımı**

İyi bir system prompt içermeli:
- ✅ Bot'un rolü ve kimliği
- ✅ Görev tanımları
- ✅ İşletme bilgileri (adres, telefon, saatler)
- ✅ Fiyat bilgileri
- ✅ Özel durumlar ve kurallar
- ✅ İletişim tonu (nazik, profesyonel)

### 3. **Oturum Yönetimi**

- "Beni Hatırla" işaretlerseniz 30 gün oturum açık kalır
- İşaretlemezseniz tarayıcı kapanınca oturum sona erer
- Çıkış yapmayı unutmayın (özellikle paylaşımlı bilgisayarlarda)

---

## 🎯 Sonraki Özellikler

- [ ] Şifre sıfırlama
- [ ] 2FA (Two-Factor Authentication)
- [ ] Oturum geçmişi
- [ ] Bot performans metrikleri
- [ ] Sohbet geçmişi görüntüleme
- [ ] API kullanım istatistikleri
- [ ] Çoklu dil desteği
- [ ] Dark mode

---

## 📞 Destek

Sorunlarla karşılaşırsanız:

1. Tarayıcı console'u kontrol edin (F12)
2. Server loglarını inceleyin
3. Session temizleyin ve tekrar deneyin
4. Demo kullanıcıyı yeniden oluşturun

---

🇹🇷 **Tamamen Türkçe Arayüz - Türk Pazarına Özel**
