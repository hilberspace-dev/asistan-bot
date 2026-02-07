"""
Test script for AI Service functionality
Demonstrates how to use the AI service with different scenarios
"""
import requests
import json
from typing import Dict, List


BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response: requests.Response):
    """Pretty print API response"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print("-" * 70)


def test_tenant_info(tenant_id: int = 1):
    """Test getting tenant AI info"""
    print_section(f"1. Get Tenant AI Info (Tenant ID: {tenant_id})")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tenant/{tenant_id}/info")
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Tenant info retrieved successfully")
            print(f"   Business: {data['tenant_info']['business_name']}")
            print(f"   Has API Key: {data['tenant_info']['has_api_key']}")
            return True
        else:
            print("❌ Failed to get tenant info")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_validate_api_key(tenant_id: int = 1):
    """Test validating tenant's API key"""
    print_section(f"2. Validate API Key (Tenant ID: {tenant_id})")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tenant/{tenant_id}/validate")
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("api_key_valid"):
                print("✅ API key is valid and working")
            else:
                print("⚠️  API key validation failed")
            return data.get("api_key_valid", False)
        else:
            print("❌ Failed to validate API key")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_models(tenant_id: int = 1):
    """Test getting available models"""
    print_section(f"3. Get Available Models (Tenant ID: {tenant_id})")
    
    try:
        response = requests.get(f"{BASE_URL}/api/tenant/{tenant_id}/models")
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Available models retrieved")
            print(f"   Models: {', '.join(data['available_models'])}")
            return True
        else:
            print("❌ Failed to get models")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_simple_chat(tenant_id: int = 1):
    """Test simple chat completion"""
    print_section(f"4. Simple Chat Completion (Tenant ID: {tenant_id})")
    
    chat_request = {
        "tenant_id": tenant_id,
        "user_message": "Merhaba! Saat kaçta açıksınız?",
        "model": "gpt-4o-mini",
        "temperature": 0.7
    }
    
    print(f"\n📝 User Message: {chat_request['user_message']}")
    print(f"🤖 Model: {chat_request['model']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=chat_request
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Chat completion successful!")
            print(f"\n👤 User: {data['user_message']}")
            print(f"🤖 Assistant: {data['assistant_message']}")
            print(f"\n📊 Business: {data['business_name']}")
            print(f"📊 Model: {data['model']}")
            return True
        else:
            print_response(response)
            print("❌ Chat completion failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_chat_with_history(tenant_id: int = 1):
    """Test chat with conversation history"""
    print_section(f"5. Chat with Conversation History (Tenant ID: {tenant_id})")
    
    chat_request = {
        "tenant_id": tenant_id,
        "user_message": "Peki randevu iptal etmek için ne yapmalıyım?",
        "conversation_history": [
            {
                "role": "user",
                "content": "Merhaba! Randevu almak istiyorum."
            },
            {
                "role": "assistant",
                "content": "Merhaba! Tabii ki, size yardımcı olabilirim. Hangi gün için randevu almak istersiniz?"
            }
        ],
        "model": "gpt-4o-mini",
        "temperature": 0.7
    }
    
    print("\n📜 Conversation History:")
    for msg in chat_request['conversation_history']:
        role_emoji = "👤" if msg['role'] == "user" else "🤖"
        print(f"   {role_emoji} {msg['role'].title()}: {msg['content']}")
    
    print(f"\n📝 New User Message: {chat_request['user_message']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=chat_request
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Chat completion with history successful!")
            print(f"\n🤖 Assistant: {data['assistant_message']}")
            return True
        else:
            print_response(response)
            print("❌ Chat completion failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_streaming_chat(tenant_id: int = 1):
    """Test streaming chat completion"""
    print_section(f"6. Streaming Chat Completion (Tenant ID: {tenant_id})")
    
    chat_request = {
        "tenant_id": tenant_id,
        "user_message": "Klinik hizmetleri hakkında detaylı bilgi verir misiniz?",
        "model": "gpt-4o-mini",
        "temperature": 0.8,
        "stream": True
    }
    
    print(f"\n📝 User Message: {chat_request['user_message']}")
    print("\n🤖 Assistant (streaming):")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/stream",
            json=chat_request,
            stream=True
        )
        
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    print(chunk, end='', flush=True)
            
            print("\n" + "-" * 70)
            print("\n✅ Streaming chat completed successfully!")
            return True
        else:
            print(f"❌ Streaming failed: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_different_temperatures(tenant_id: int = 1):
    """Test chat with different temperature settings"""
    print_section(f"7. Testing Different Temperatures (Tenant ID: {tenant_id})")
    
    temperatures = [0.3, 0.7, 1.2]
    user_message = "Bugün hava nasıl?"
    
    for temp in temperatures:
        print(f"\n🌡️ Temperature: {temp}")
        
        chat_request = {
            "tenant_id": tenant_id,
            "user_message": user_message,
            "model": "gpt-4o-mini",
            "temperature": temp
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json=chat_request
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Response: {data['assistant_message'][:100]}...")
            else:
                print(f"❌ Failed with temp {temp}")
                
        except Exception as e:
            print(f"❌ Error: {e}")


def test_error_handling(tenant_id: int = 999):
    """Test error handling with non-existent tenant"""
    print_section(f"8. Error Handling - Non-existent Tenant (ID: {tenant_id})")
    
    chat_request = {
        "tenant_id": tenant_id,
        "user_message": "Test message",
        "model": "gpt-4o-mini"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=chat_request
        )
        
        print_response(response)
        
        if response.status_code == 400:
            print("✅ Error handling working correctly (400 Bad Request)")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests"""
    print("\n" + "🧪" * 35)
    print("   AI SERVICE COMPREHENSIVE TEST SUITE")
    print("🧪" * 35)
    
    # Check server health
    print_section("0. Server Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return
    except:
        print("❌ Cannot connect to server. Please run: python main.py")
        return
    
    # Test with demo tenant (ID: 1)
    tenant_id = 1
    
    # Run tests
    test_tenant_info(tenant_id)
    test_get_models(tenant_id)
    
    # Validate API key first
    api_key_valid = test_validate_api_key(tenant_id)
    
    if api_key_valid:
        print("\n✅ API key is valid - proceeding with chat tests")
        test_simple_chat(tenant_id)
        test_chat_with_history(tenant_id)
        test_streaming_chat(tenant_id)
        test_different_temperatures(tenant_id)
    else:
        print("\n⚠️  API key validation failed - skipping chat tests")
        print("   Please update the demo user with a valid OpenAI API key")
        print("   You can do this through the admin panel: http://localhost:8000/giris")
    
    # Test error handling
    test_error_handling()
    
    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print("\n✅ All tests completed!")
    print("\n📋 Quick Usage Guide:")
    print("   1. Ensure demo user has valid OpenAI API key")
    print("   2. Use POST /api/chat for standard completions")
    print("   3. Use POST /api/chat/stream for streaming responses")
    print("   4. Include conversation_history for context")
    print("   5. Adjust temperature (0.0-2.0) for creativity")
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
