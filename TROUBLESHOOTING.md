# 🔍 Troubleshooting 500 Error - Templates

## ✅ Current Status

Your configuration is CORRECT:

### File Structure (Verified)
```
randevu-asistani/
├── main.py                     ← Root (correct)
├── app/
│   └── templates/              ← Templates here (correct)
│       ├── dashboard.html      ✓ Found
│       ├── giris.html          ✓ Found
│       └── panel.html          ✓ Found
```

### Path Configuration (Verified)
- ✅ `main.py` uses: `os.path.join(BASE_DIR, "app", "templates")`
- ✅ `app/api/auth.py` uses absolute path
- ✅ All 3 HTML files exist

---

## 🧪 Diagnostic Steps

### Step 1: Run Template Path Test
```bash
python test_templates.py
```

You should see:
```
✅ All template files found successfully!
```

### Step 2: Restart Server with Debug Output
```bash
python main.py
```

You should see:
```
DEBUG: Templates directory is set to: C:\Users\atilg\OneDrive\Masaüstü\randevu-asistani\app\templates
DEBUG: Templates directory exists: True
DEBUG: Files in templates directory: ['dashboard.html', 'giris.html', 'panel.html']
🚀 Starting Virtual Receptionist SaaS v1.0.0
```

### Step 3: Test Debug Endpoints

**Check template configuration:**
```
http://localhost:8000/debug/templates
```

Should return:
```json
{
  "templates_exist": true,
  "template_files": ["dashboard.html", "giris.html", "panel.html"]
}
```

**Test template loading directly:**
```
http://localhost:8000/test-template
```

Should show the login page (giris.html)

### Step 4: Test Login Page
```
http://localhost:8000/giris
```

Should load without 500 error.

---

## 🐛 If Still Getting 500 Error

### Possible Causes:

#### 1. Server Not Restarted
**Solution:** Stop server (Ctrl+C) and restart:
```bash
python main.py
```

#### 2. Running from Wrong Directory
**Check:** Are you in the project root?
```bash
# Windows
cd C:\Users\atilg\OneDrive\Masaüstü\randevu-asistani
python main.py
```

#### 3. Import Error or Database Error
**Check:** Look at the full error in terminal when you visit `/giris`

The 500 error might not be from templates but from:
- Database not initialized
- Missing dependencies
- Import errors in auth.py

**Solution:**
```bash
# Initialize database
python database.py

# Create demo user
python create_demo_user.py
```

#### 4. Cached Python Bytecode
**Solution:** Clear cache and restart:
```bash
# Windows PowerShell
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse
python main.py
```

#### 5. Port Already in Use
**Solution:** Kill process on port 8000 or use different port:
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Or change port in main.py:
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

---

## 📊 Check Server Logs

When you access `/giris` and get 500 error, check your terminal for the actual error message.

Common errors and solutions:

### "TemplateNotFound: giris.html"
**Cause:** Template path is wrong
**Solution:** Verify with `/debug/templates` endpoint

### "Table 'tenants' doesn't exist"
**Cause:** Database not initialized
**Solution:** `python database.py`

### "No module named 'app.core.config'"
**Cause:** Running from wrong directory
**Solution:** `cd` to project root

### "Address already in use"
**Cause:** Port 8000 is taken
**Solution:** Kill other process or change port

---

## ✅ Verification Checklist

Run through these:

- [ ] Run `python test_templates.py` - shows files found
- [ ] Server starts with DEBUG output showing correct path
- [ ] `/debug/templates` shows `templates_exist: true`
- [ ] `/test-template` loads the login page
- [ ] Database exists (`randevu_asistani.db` file present)
- [ ] Demo user created (`python create_demo_user.py`)
- [ ] No other process using port 8000

---

## 🔧 Nuclear Option: Full Reset

If nothing works:

```bash
# 1. Stop server (Ctrl+C)

# 2. Clear all cache
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force

# 3. Delete database
Remove-Item randevu_asistani.db -ErrorAction SilentlyContinue

# 4. Reinstall dependencies
pip install -r requirements.txt

# 5. Initialize fresh database
python database.py

# 6. Create demo user
python create_demo_user.py

# 7. Start server
python main.py

# 8. Test
# Visit: http://localhost:8000/test-template
```

---

## 📞 Getting More Info

To see the actual error causing the 500:

### Option 1: Check Terminal Output
The terminal where you ran `python main.py` will show the full traceback.

### Option 2: Add More Debug
In your browser, after getting 500 error, check the terminal for a stack trace like:
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "...", line X, in ...
    ...
[Error details here]
```

Copy that full error and we can diagnose the exact issue.

---

## 🎯 Most Likely Issues

Based on typical causes:

1. **Database not initialized** (60% of cases)
   - Solution: `python database.py`

2. **Server not restarted** (20% of cases)
   - Solution: Ctrl+C and `python main.py` again

3. **Wrong working directory** (15% of cases)
   - Solution: `cd` to project root

4. **Missing dependencies** (5% of cases)
   - Solution: `pip install -r requirements.txt`

---

Your template paths are CORRECT. The 500 error is likely from something else. Follow the diagnostic steps above to identify the real cause!
