"""
Quick test script to verify template paths
Run this to see if templates can be found
"""
import os

# Same logic as main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(BASE_DIR, "app", "templates")

print("=" * 60)
print("TEMPLATE PATH TEST")
print("=" * 60)
print()
print(f"Script location: {__file__}")
print(f"BASE_DIR: {BASE_DIR}")
print(f"Templates path: {templates_path}")
print()
print(f"Templates directory exists: {os.path.exists(templates_path)}")
print()

if os.path.exists(templates_path):
    print("Files in templates directory:")
    for file in os.listdir(templates_path):
        file_path = os.path.join(templates_path, file)
        print(f"  ✓ {file} ({os.path.getsize(file_path)} bytes)")
    print()
    print("✅ All template files found successfully!")
else:
    print("❌ ERROR: Templates directory not found!")
    print()
    print("Current working directory:", os.getcwd())
    print()
    print("Looking for templates in these locations:")
    possible_paths = [
        os.path.join(BASE_DIR, "templates"),
        os.path.join(BASE_DIR, "app", "templates"),
        os.path.join(os.getcwd(), "templates"),
        os.path.join(os.getcwd(), "app", "templates"),
    ]
    for path in possible_paths:
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"  {exists} {path}")

print()
print("=" * 60)
