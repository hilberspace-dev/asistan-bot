"""
Script to move templates from app/templates to root templates/ folder
Run this if you're getting template errors after the fix
"""
import os
import shutil
from pathlib import Path


def move_templates():
    """Move templates from app/templates to root templates/"""
    
    # Define paths
    source_dir = Path("app/templates")
    dest_dir = Path("templates")
    
    print("🔍 Checking template locations...")
    print()
    
    # Check if source exists
    if not source_dir.exists():
        print("ℹ️  app/templates/ directory doesn't exist")
        if dest_dir.exists():
            print("✅ templates/ directory already exists in root")
            print("   Your templates are already in the correct location!")
        else:
            print("⚠️  Neither app/templates/ nor templates/ exists")
            print("   Please create templates/ folder and add your HTML files")
        return
    
    # Check if destination exists
    if dest_dir.exists():
        print("⚠️  Both app/templates/ and templates/ exist")
        print("   Please manually resolve this:")
        print("   1. Check which folder has the correct files")
        print("   2. Delete the incorrect folder")
        print("   3. Ensure templates/ in root has: dashboard.html, giris.html, panel.html")
        return
    
    # Move templates
    try:
        print(f"📦 Moving templates from {source_dir} to {dest_dir}...")
        shutil.move(str(source_dir), str(dest_dir))
        print("✅ Templates moved successfully!")
        print()
        print("📁 New structure:")
        print("   templates/")
        
        # List moved files
        if dest_dir.exists():
            for file in dest_dir.glob("*.html"):
                print(f"   ├── {file.name}")
        
        print()
        print("🎉 Done! Restart your server:")
        print("   python main.py")
        
    except Exception as e:
        print(f"❌ Error moving templates: {e}")
        print()
        print("💡 Manual steps:")
        print("   1. Create 'templates' folder in project root")
        print("   2. Copy all .html files from app/templates/ to templates/")
        print("   3. Delete app/templates/ folder")


if __name__ == "__main__":
    print("=" * 60)
    print("  TEMPLATE MIGRATION SCRIPT")
    print("=" * 60)
    print()
    move_templates()
    print()
    print("=" * 60)
