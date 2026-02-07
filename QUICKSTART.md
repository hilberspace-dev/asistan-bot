# 🚀 Quick Start Guide

Hızlıca başlamak için bu adımları takip edin!

## 📦 1. Kurulum (5 dakika)

### Windows PowerShell

```powershell
# 1. Sanal ortam oluştur
python -m venv venv

# 2. Aktive et
.\venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Environment dosyasını hazırla
copy .env.example .env
```

### Linux/Mac Terminal

```bash
# 1. Sanal ortam oluştur
python3 -m venv venv

# 2. Aktive et
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Environment dosyasını hazırla
cp .env.example .env
```

## 🔑 2. Şifreleme Anahtarı Oluştur

```bash
# Yeni bir encryption key oluştur
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Bu komutu çalıştırın ve çıktıdaki anahtarı kopyalayın. Örnek:

```
gAAAAABl...
```

`.env` dosyasını açın ve `ENCRYPTION_KEY` satırına bu anahtarı yapıştırın:

```
ENCRYPTION_KEY=gAAAAABl...
```

## 🗄️ 3. Veritabanını Başlat

```bash
python database.py
```

Çıktı:
```
🔧 Initializing database...
✅ Database initialized successfully
```

## ▶️ 4. Sunucuyu Başlat

```bash
python main.py
```

Çıktı:
```
🚀 Starting Virtual Receptionist SaaS v1.0.0
✅ Database initialized successfully
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🌐 5. Uygulamayı Aç

Tarayıcınızda şu adresleri açın:

- **Ana Sayfa**: http://localhost:8000
- **Admin Girişi**: http://localhost:8000/giris 👈 **Buradan başlayın!**
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## 👤 6. Demo Kullanıcı Oluştur

```bash
python create_demo_user.py
```

Çıktı:
```
✅ Demo user created successfully!

📋 Login Credentials:
   URL: http://localhost:8000/giris
   Username: demo
   Password: demo123
```

## 🧪 7. API'yi Test Et

### Yöntem 1: Admin Panel (Önerilen) 🌟

1. http://localhost:8000/giris adresine gidin
2. Demo kullanıcı ile giriş yapın:
   - **Kullanıcı Adı**: demo
   - **Şifre**: demo123
3. Yönetim panelinde ayarları görüntüleyin ve düzenleyin
4. "Ayarları Kaydet" butonuna tıklayın
5. Başarı bildirimi görünecek

### Yöntem 2: Web Tarayıcısı (API Docs)

1. http://localhost:8000/docs adresine gidin
2. `POST /api/tenants/` endpoint'ini genişletin
3. "Try it out" butonuna tıklayın
4. Örnek veriyi düzenleyin ve "Execute" butonuna basın

### Yöntem 3: Python Test Script

Admin panel testleri için:

```bash
python test_admin_panel.py
```

Bu script otomatik olarak:
- ✅ Server sağlık kontrolü
- ✅ Login sayfası testi
- ✅ Yanlış şifre testi
- ✅ Başarılı login testi
- ✅ Panel güncelleme testi
- ✅ Logout testi

API testleri için:

```bash
python example_usage.py
```

### Yöntem 4: cURL

```bash
# Health check
curl http://localhost:8000/health

# Yeni müşteri oluştur
curl -X POST "http://localhost:8000/api/tenants/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"test_user\",\"password\":\"test123\",\"business_name\":\"Test İşletme\",\"openai_api_key\":\"sk-test\",\"system_prompt\":\"Test prompt\"}"

# Tüm müşterileri listele
curl http://localhost:8000/api/tenants/
```

## 📊 7. Dashboard'u Kullan

### Ana Sayfa
http://localhost:8000 adresine gidin:
- 📈 İstatistikler
- 📋 Özellikler listesi
- 🔌 API endpoints
- 💡 Hızlı başlangıç kılavuzu

### Admin Panel (Yönetim Paneli) ⭐
http://localhost:8000/giris adresine gidin:

#### Login Sayfası
- ✅ Kullanıcı adı: `demo`
- ✅ Şifre: `demo123`
- ✅ "Beni Hatırla" seçeneği
- ✅ Tamamen Türkçe arayüz

#### Dashboard Panel
Giriş yaptıktan sonra:
- 🤖 Hoşgeldin mesajı
- ⚙️ **OpenAI API Anahtarı** (şifreli gösterim)
- 📝 **Bot Talimatları** (system prompt)
- 🏢 **İşletme Adı** düzenleme
- 💾 **Ayarları Kaydet** butonu
- 📊 Durum kartları (Aktif, API Bağlı, vb.)
- 🚪 Çıkış butonu

Detaylı kullanım: [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md)

## ✅ Tebrikler!

Başarıyla kurulum yaptınız! Artık Virtual Receptionist SaaS sisteminiz hazır.

## 🔍 Sonraki Adımlar

1. **Gerçek OpenAI API Key Kullanın**: Gerçek bir işletme için test ederken, geçerli bir OpenAI API anahtarı kullanın
2. **System Prompt'u Özelleştirin**: Her işletme için özel talimatlar yazın
3. **WhatsApp Entegrasyonu**: Sanal asistanı WhatsApp'a bağlayın (gelecek özellik)
4. **Dashboard Geliştirme**: Admin paneli ekleyin

## 🐛 Sorun Giderme

### "Module not found" hatası

```bash
# Bağımlılıkları tekrar yükleyin
pip install -r requirements.txt
```

### Veritabanı hatası

```bash
# Veritabanını sıfırlayın
python database.py reset
```

### Port zaten kullanımda

```bash
# main.py'de portu değiştirin (örn: 8001)
# veya 8000 portunu kullanan uygulamayı kapatın
```

## 📞 Destek

Herhangi bir sorunla karşılaşırsanız:

1. README.md dosyasını okuyun
2. API dokümantasyonunu inceleyin: http://localhost:8000/docs
3. Log dosyalarını kontrol edin

---

🎉 **Keyifli kodlamalar!**
