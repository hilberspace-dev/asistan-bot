"""
Example usage script for Virtual Receptionist SaaS API
Demonstrates how to interact with the tenant management endpoints
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def print_response(response):
    """Pretty print API response"""
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print("-" * 50)


def main():
    print("🤖 Virtual Receptionist SaaS - API Usage Examples\n")
    
    # 1. Health Check
    print("1️⃣ Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    
    # 2. Create a new tenant
    print("2️⃣ Creating a new tenant (Ahmet Diş Kliniği)")
    tenant_data = {
        "username": "ahmet_dis_klinigi",
        "password": "guvenli_sifre_123",
        "business_name": "Ahmet Diş Kliniği",
        "openai_api_key": "sk-proj-test-key-12345",
        "system_prompt": """Sen Ahmet Diş Kliniği'nin sanal resepsiyonistisin.
Görevlerin:
- Randevu almak
- Randevu iptal etmek veya değiştirmek
- Klinik hakkında bilgi vermek
- Tedavi hizmetleri hakkında bilgi vermek

Her zaman nazik, profesyonel ve yardımsever ol. 
Müşterilere saygılı ve anlayışlı davran."""
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tenants/",
        json=tenant_data
    )
    print_response(response)
    
    if response.status_code == 201:
        tenant_id = response.json()["id"]
        print(f"✅ Tenant created with ID: {tenant_id}\n")
        
        # 3. Get tenant details
        print("3️⃣ Getting tenant details")
        response = requests.get(f"{BASE_URL}/api/tenants/{tenant_id}")
        print_response(response)
        
        # 4. Update tenant
        print("4️⃣ Updating tenant business name")
        update_data = {
            "business_name": "Ahmet Diş Kliniği - Merkez Şubesi"
        }
        response = requests.put(
            f"{BASE_URL}/api/tenants/{tenant_id}",
            json=update_data
        )
        print_response(response)
        
        # 5. List all tenants
        print("5️⃣ Listing all tenants")
        response = requests.get(f"{BASE_URL}/api/tenants/")
        print_response(response)
        
        # 6. Create another tenant
        print("6️⃣ Creating another tenant (Ayşe Güzellik Salonu)")
        tenant_data2 = {
            "username": "ayse_guzellik",
            "password": "super_guvenli_456",
            "business_name": "Ayşe Güzellik Salonu",
            "openai_api_key": "sk-proj-test-key-67890",
            "system_prompt": "Sen Ayşe Güzellik Salonu'nun sanal asistanısın. Randevu al ve müşterilere yardımcı ol."
        }
        
        response = requests.post(
            f"{BASE_URL}/api/tenants/",
            json=tenant_data2
        )
        print_response(response)
        
        # 7. List all tenants again
        print("7️⃣ Listing all tenants (should show 2)")
        response = requests.get(f"{BASE_URL}/api/tenants/")
        print_response(response)
        
        # Optional: Delete tenant (uncomment to test)
        # print("8️⃣ Deleting first tenant")
        # response = requests.delete(f"{BASE_URL}/api/tenants/{tenant_id}")
        # print(f"Status Code: {response.status_code}")
        # print("✅ Tenant deleted" if response.status_code == 204 else "❌ Delete failed")
        
    else:
        print("❌ Failed to create tenant. Make sure the server is running!")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
