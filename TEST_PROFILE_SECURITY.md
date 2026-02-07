# 🧪 Profile & Security - Test Guide

## ✅ Prerequisites

**Ensure passlib is installed:**
```bash
pip install passlib[bcrypt]
```

**Restart server:**
```bash
python main.py
```

---

## 🧪 Test Scenarios

### **Test 1: Wrong Current Password (Should Fail)**

1. Login: `http://localhost:8000/giris`
   - Username: `demo`
   - Password: `123`

2. Go to panel (automatically redirected)

3. Scroll to **"🔐 Hesap Ayarları"** section

4. Fill form:
   - Mevcut Şifre: `WRONG_PASSWORD`
   - Yeni Kullanıcı Adı: `test`
   - Yeni Şifre: (leave blank)

5. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
❌ Mevcut şifre hatalı!
```

---

### **Test 2: Change Username (Should Succeed)**

1. Fill form:
   - Mevcut Şifre: `123`
   - Yeni Kullanıcı Adı: `admin`
   - Yeni Şifre: (leave blank)

2. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
✅ Hesap bilgileriniz başarıyla güncellendi!
```

**Verify:**
- Navbar should show: `admin` (instead of `demo`)
- Logout and try login with:
  - Username: `admin` (NEW)
  - Password: `123` (unchanged)

---

### **Test 3: Change Password (Should Succeed)**

1. Login with current credentials

2. Fill form:
   - Mevcut Şifre: `123`
   - Yeni Kullanıcı Adı: (leave as is)
   - Yeni Şifre: `secure456`

3. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
✅ Hesap bilgileriniz başarıyla güncellendi!
```

**Verify:**
- Logout
- Try login with OLD password `123` → Should FAIL
- Try login with NEW password `secure456` → Should SUCCESS
- Password should be HASHED in database (check with DB viewer)

---

### **Test 4: Change Both (Should Succeed)**

1. Login with current credentials

2. Fill form:
   - Mevcut Şifre: `secure456`
   - Yeni Kullanıcı Adı: `superadmin`
   - Yeni Şifre: `ultra_secure_789`

3. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
✅ Hesap bilgileriniz başarıyla güncellendi!
```

**Verify:**
- Navbar shows: `superadmin`
- Logout
- Login with:
  - Username: `superadmin`
  - Password: `ultra_secure_789`

---

### **Test 5: Duplicate Username (Should Fail)**

1. Create second user via API or demo script

2. Try to change username to existing one

3. Fill form:
   - Mevcut Şifre: `123`
   - Yeni Kullanıcı Adı: `existing_username`

4. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
❌ Bu kullanıcı adı zaten kullanılıyor!
```

---

### **Test 6: Leave Everything Blank Except Current Password**

1. Fill form:
   - Mevcut Şifre: `123`
   - Yeni Kullanıcı Adı: (leave as is)
   - Yeni Şifre: (leave blank)

2. Click **"Bilgileri Güncelle"**

**Expected Result:**
```
✅ Hesap bilgileriniz başarıyla güncellendi!
```

**Verify:**
- Nothing changes (username and password remain the same)
- This is valid behavior (user verified password but didn't change anything)

---

## 🔍 Verify Password Hashing

**Check database to confirm passwords are hashed:**

```python
# Quick check script
from main import SessionLocal, Tenant

db = SessionLocal()
user = db.query(Tenant).filter(Tenant.username == "demo").first()
print(f"Password in DB: {user.password}")
# Should show: "$2b$12$..." (bcrypt hash)
# NOT: "123" (plain text)
db.close()
```

**Bcrypt hash format:**
```
$2b$12$abcdefghijk...
```
- `$2b$` = bcrypt algorithm
- `$12$` = cost factor (12 rounds)
- Rest = salt + hash

---

## 🎨 UI Elements

### **Form Fields:**
1. **Mevcut Şifre** (Current Password)
   - Type: password
   - Required: ✅ Yes
   - Placeholder: "Güvenlik için mevcut şifrenizi girin"
   - Helper text: "Değişiklik yapmak için önce mevcut şifrenizi doğrulamalısınız."

2. **Yeni Kullanıcı Adı** (New Username)
   - Type: text
   - Required: ❌ No
   - Pre-filled: Current username
   - Placeholder: "Yeni kullanıcı adı (boş bırakırsanız değişmez)"

3. **Yeni Şifre** (New Password)
   - Type: password
   - Required: ❌ No
   - Placeholder: "Yeni şifre (boş bırakırsanız değişmez)"
   - Helper text: "Boş bırakırsanız mevcut şifreniz korunur."

### **Error Messages (Turkish):**
- "❌ Mevcut şifre hatalı!"
- "❌ Bu kullanıcı adı zaten kullanılıyor!"

### **Success Message:**
- "✅ Hesap bilgileriniz başarıyla güncellendi!"

---

## 📊 API Endpoint

**POST /update-credentials**

**Form Data:**
```
current_password: string (required)
new_username: string (optional)
new_password: string (optional)
```

**Responses:**
- ✅ Success → Panel with success message
- ❌ Wrong password → Panel with error message
- ❌ Duplicate username → Panel with error message

---

## 🎉 Summary

**Feature:** ✅ Complete  
**Security:** ✅ Password verification required  
**Hashing:** ✅ bcrypt with automatic salt  
**UI:** ✅ Professional Turkish interface  
**Testing:** ✅ All scenarios covered  

**Users can now safely change their credentials!** 🔐

---

🇹🇷 **Tamamen Türkçe - Güvenli Hesap Yönetimi**
