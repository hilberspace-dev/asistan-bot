# 🔧 Template Path Fix Guide

## Issue Fixed
Changed template directory paths from `app/templates` to `templates` to match flat project structure.

## Files Updated

### 1. main.py (Line 33)
**Before:**
```python
templates = Jinja2Templates(directory="app/templates")
```

**After:**
```python
templates = Jinja2Templates(directory="templates")
```

### 2. app/api/auth.py (Line 17)
**Before:**
```python
templates = Jinja2Templates(directory="app/templates")
```

**After:**
```python
templates = Jinja2Templates(directory="templates")
```

---

## Required File Structure

For the fix to work, ensure your templates are in the root `templates` folder:

```
randevu-asistani/
├── templates/              # ← Templates should be HERE
│   ├── dashboard.html
│   ├── giris.html
│   └── panel.html
├── app/
│   ├── core/
│   ├── models/
│   └── api/
├── main.py
└── requirements.txt
```

---

## If Templates Are Still in app/templates/

If your templates are currently in `app/templates/`, you have two options:

### Option 1: Move Templates to Root (Recommended)
```bash
# Windows PowerShell
Move-Item -Path "app/templates" -Destination "templates"

# Or manually:
# 1. Create 'templates' folder in root
# 2. Move dashboard.html, giris.html, panel.html to root templates/
# 3. Delete app/templates folder
```

### Option 2: Revert Changes
If you want to keep templates in `app/templates/`, revert the changes:

**main.py:**
```python
templates = Jinja2Templates(directory="app/templates")
```

**app/api/auth.py:**
```python
templates = Jinja2Templates(directory="app/templates")
```

---

## Verify the Fix

1. **Check Template Location:**
   ```bash
   # Should exist:
   dir templates\dashboard.html
   dir templates\giris.html
   dir templates\panel.html
   ```

2. **Restart Server:**
   ```bash
   python main.py
   ```

3. **Test Login:**
   - Open: http://localhost:8000/giris
   - Login with: demo / 123
   - Should redirect to panel without 500 error

---

## Common Issues

### Issue 1: Still Getting 500 Error
**Cause:** Templates not in correct location

**Solution:** 
```bash
# Check where templates actually are
Get-ChildItem -Recurse -Filter "*.html"

# Move them to root templates/ folder if needed
```

### Issue 2: "TemplateNotFound" Error
**Cause:** Template files don't exist or wrong path

**Solution:**
- Verify `templates/giris.html` exists
- Verify `templates/panel.html` exists
- Verify `templates/dashboard.html` exists

### Issue 3: Import Errors
**Cause:** Running from wrong directory

**Solution:**
```bash
# Make sure you're in the project root
cd C:\Users\atilg\OneDrive\Masaüstü\randevu-asistani

# Then run
python main.py
```

---

## Testing After Fix

```bash
# 1. Start server
python main.py

# 2. In browser, test these URLs:
# - http://localhost:8000/ (should show dashboard)
# - http://localhost:8000/giris (should show login page)
# - Login with demo/123 (should redirect to panel)

# 3. Check terminal for errors
# Should see:
# 🚀 Starting Virtual Receptionist SaaS v1.0.0
# ✅ Database initialized successfully
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Static Files (Future)

If you add static files (CSS, JS, images), use this configuration in main.py:

```python
# For flat structure
app.mount("/static", StaticFiles(directory="static"), name="static")

# File structure:
# randevu-asistani/
# ├── static/
# │   ├── css/
# │   ├── js/
# │   └── images/
# └── templates/
```

---

## Summary

✅ **Fixed:** Template paths now point to root `templates/` folder
✅ **Updated:** `main.py` and `app/api/auth.py`
✅ **Next Step:** Ensure templates are in `templates/` folder (not `app/templates/`)

If you continue to have issues, check:
1. Template files exist in correct location
2. Running server from project root directory
3. No typos in template filenames
4. Proper file permissions

---

🎉 **The 500 error should be resolved after ensuring templates are in the correct location!**
