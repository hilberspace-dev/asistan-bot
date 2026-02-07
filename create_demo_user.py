"""
Create a demo user for testing the admin panel
"""
from app.core.database import SessionLocal, init_db
from app.core.security import get_password_hash
from app.models.tenant import Tenant


def create_demo_user():
    """Create a demo tenant user for testing"""
    # Initialize database
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if demo user already exists
        existing_user = db.query(Tenant).filter(Tenant.username == "demo").first()
        
        if existing_user:
            print("⚠️  Demo user already exists!")
            print(f"   Username: demo")
            print(f"   Password: 123")
            print(f"   Business: {existing_user.business_name}")
            return
        
        # Create demo tenant
        demo_tenant = Tenant(
            username="demo",
            password_hash=get_password_hash("123"),
            business_name="Demo Estetik Kliniği",
            system_prompt="Biz lüks bir kliniğiz. Botox 1000 TL."
        )
        
        # Set encrypted API key
        demo_tenant.set_openai_api_key("sk-proj-demo-key-12345678901234567890")
        
        # Add to database
        db.add(demo_tenant)
        db.commit()
        db.refresh(demo_tenant)
        
        print("✅ Demo user created successfully!")
        print()
        print("📋 Login Credentials:")
        print("   URL: http://localhost:8000/giris")
        print("   Username: demo")
        print("   Password: 123")
        print()
        print("🎯 Test the admin panel:")
        print("   1. Start the server: python main.py")
        print("   2. Open: http://localhost:8000/giris")
        print("   3. Login with the credentials above")
        print("   4. Manage your bot settings in the panel!")
        print()
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_demo_user()
