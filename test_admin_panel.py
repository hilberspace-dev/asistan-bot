"""
Comprehensive test script for Admin Panel functionality
Tests the complete authentication and settings management flow
"""
import requests
from requests.exceptions import ConnectionError


BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health():
    """Test health check endpoint"""
    print_section("1. Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is healthy")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        return True
    except ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Run: python main.py")
        return False


def test_login_page():
    """Test login page accessibility"""
    print_section("2. Testing Login Page (GET)")
    try:
        response = requests.get(f"{BASE_URL}/giris")
        if response.status_code == 200:
            print("✅ Login page accessible")
            if "Yönetim Paneli Giriş" in response.text:
                print("✅ Turkish text verified: 'Yönetim Paneli Giriş'")
            if "Kullanıcı Adı" in response.text:
                print("✅ Form field verified: 'Kullanıcı Adı'")
            if "Şifre" in response.text:
                print("✅ Form field verified: 'Şifre'")
            if "Giriş Yap" in response.text:
                print("✅ Button verified: 'Giriş Yap'")
        else:
            print(f"❌ Login page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_login_wrong_credentials():
    """Test login with wrong credentials"""
    print_section("3. Testing Login with Wrong Credentials")
    try:
        session = requests.Session()
        response = session.post(
            f"{BASE_URL}/giris",
            data={
                "username": "wrong_user",
                "password": "wrong_password"
            },
            allow_redirects=False
        )
        
        if response.status_code == 401 or "hatalı" in response.text.lower():
            print("✅ Wrong credentials rejected")
            if "Kullanıcı adı veya şifre hatalı" in response.text:
                print("✅ Turkish error message verified")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_login_success():
    """Test successful login"""
    print_section("4. Testing Successful Login")
    try:
        session = requests.Session()
        
        # Login
        response = session.post(
            f"{BASE_URL}/giris",
            data={
                "username": "demo",
                "password": "demo123",
                "remember": "on"
            },
            allow_redirects=False
        )
        
        if response.status_code == 302 and response.headers.get("location") == "/panel":
            print("✅ Login successful")
            print("✅ Redirected to /panel")
            
            # Try to access panel
            panel_response = session.get(f"{BASE_URL}/panel")
            if panel_response.status_code == 200:
                print("✅ Panel accessible after login")
                
                # Verify Turkish content
                if "Hoşgeldiniz" in panel_response.text:
                    print("✅ Welcome message verified: 'Hoşgeldiniz'")
                if "Yapay Zeka Ayarları" in panel_response.text:
                    print("✅ Settings section verified: 'Yapay Zeka Ayarları'")
                if "OpenAI API Anahtarı" in panel_response.text:
                    print("✅ API Key field verified: 'OpenAI API Anahtarı'")
                if "Bot Talimatları" in panel_response.text:
                    print("✅ System Prompt field verified: 'Bot Talimatları'")
                if "Ayarları Kaydet" in panel_response.text:
                    print("✅ Save button verified: 'Ayarları Kaydet'")
                
                return session
            else:
                print(f"❌ Cannot access panel: {panel_response.status_code}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Location: {response.headers.get('location')}")
        
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_panel_update(session):
    """Test panel settings update"""
    print_section("5. Testing Panel Settings Update")
    try:
        if not session:
            print("⚠️  No active session, skipping test")
            return
        
        # Update settings
        response = session.post(
            f"{BASE_URL}/panel",
            data={
                "api_key": "",  # Keep existing (empty = no change)
                "system_prompt": "Test: Bot talimatları güncellendi. Pazar günleri kapalıyız.",
                "business_name": "Test İşletme Güncellemesi"
            }
        )
        
        if response.status_code == 200:
            print("✅ Settings updated successfully")
            
            if "Başarıyla Kaydedildi" in response.text or "başarıyla" in response.text.lower():
                print("✅ Success notification verified")
            
            if "Test İşletme Güncellemesi" in response.text:
                print("✅ Business name update verified")
            
            if "Test: Bot talimatları güncellendi" in response.text:
                print("✅ System prompt update verified")
        else:
            print(f"❌ Update failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_panel_without_auth():
    """Test panel access without authentication"""
    print_section("6. Testing Panel Access Without Auth")
    try:
        # Try to access panel without session
        response = requests.get(f"{BASE_URL}/panel", allow_redirects=False)
        
        if response.status_code == 302 and response.headers.get("location") == "/giris":
            print("✅ Unauthorized access blocked")
            print("✅ Redirected to login page")
        else:
            print(f"⚠️  Security issue: Panel accessible without auth")
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_logout(session):
    """Test logout functionality"""
    print_section("7. Testing Logout")
    try:
        if not session:
            print("⚠️  No active session, skipping test")
            return
        
        # Logout
        response = session.get(f"{BASE_URL}/cikis", allow_redirects=False)
        
        if response.status_code == 302 and response.headers.get("location") == "/giris":
            print("✅ Logout successful")
            print("✅ Redirected to login page")
            
            # Try to access panel after logout
            panel_response = session.get(f"{BASE_URL}/panel", allow_redirects=False)
            if panel_response.status_code == 302:
                print("✅ Session cleared (panel inaccessible)")
            else:
                print("⚠️  Session might not be fully cleared")
        else:
            print(f"⚠️  Unexpected logout response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_api_endpoints():
    """Test REST API endpoints"""
    print_section("8. Testing REST API Endpoints")
    try:
        # List tenants
        response = requests.get(f"{BASE_URL}/api/tenants/")
        if response.status_code == 200:
            tenants = response.json()
            print(f"✅ API endpoint working: {len(tenants)} tenant(s) found")
            
            if tenants:
                demo_tenant = next((t for t in tenants if t["username"] == "demo"), None)
                if demo_tenant:
                    print("✅ Demo tenant found in database")
                    print(f"   ID: {demo_tenant['id']}")
                    print(f"   Business: {demo_tenant['business_name']}")
        else:
            print(f"⚠️  API endpoint issue: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests"""
    print("\n" + "🧪" * 30)
    print("   ADMIN PANEL COMPREHENSIVE TEST SUITE")
    print("🧪" * 30)
    
    # Test 1: Health Check
    if not test_health():
        print("\n❌ Server not running. Please start with: python main.py")
        return
    
    # Test 2: Login Page
    test_login_page()
    
    # Test 3: Wrong Credentials
    test_login_wrong_credentials()
    
    # Test 4: Successful Login
    session = test_login_success()
    
    # Test 5: Panel Update
    test_panel_update(session)
    
    # Test 6: Unauthorized Access
    test_panel_without_auth()
    
    # Test 7: Logout
    test_logout(session)
    
    # Test 8: API Endpoints
    test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    print("\n✅ All critical tests completed!")
    print("\n📋 Manual Testing Steps:")
    print("   1. Open http://localhost:8000/giris")
    print("   2. Login with: demo / demo123")
    print("   3. Verify Turkish interface")
    print("   4. Update settings and save")
    print("   5. Verify success notification")
    print("   6. Click logout and verify redirect")
    print("\n📖 Full Guide: See ADMIN_PANEL_GUIDE.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
