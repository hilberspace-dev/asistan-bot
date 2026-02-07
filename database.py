"""
Database utility script
Run this to initialize or reset the database
"""
from app.core.database import init_db, engine, Base
from app.models.tenant import Tenant


def reset_database():
    """Drop all tables and recreate them"""
    print("⚠️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("✅ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database reset complete!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        if confirm.lower() == "yes":
            reset_database()
        else:
            print("❌ Database reset cancelled")
    else:
        print("🔧 Initializing database...")
        init_db()
