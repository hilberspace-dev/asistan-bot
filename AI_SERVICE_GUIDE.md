# 🤖 AI Service Guide - OpenAI Integration

## 📋 Overview

The AI Service provides seamless integration with OpenAI's GPT models, with dynamic tenant-based configuration and automatic Turkish language enforcement.

---

## 🎯 Key Features

### ✅ Dynamic Tenant Configuration
- Each tenant uses their own OpenAI API key
- Automatic API key decryption from database
- Isolated client instances per tenant

### ✅ Turkish Language Enforcement
- Automatic prepending of Turkish base prompt
- Forces assistant to respond only in Turkish
- Combines base prompt with tenant-specific instructions

### ✅ Secure & Robust
- Encrypted API key storage (Fernet)
- Comprehensive error handling
- Logging for debugging and monitoring

### ✅ Flexible API
- Standard chat completions
- Streaming responses
- Conversation history support
- Configurable model, temperature, max_tokens

---

## 🏗️ Architecture

### Turkish Prompt Strategy

Every request to OpenAI includes this base prompt:

```
Sen yardımsever bir Türk asistansın. Adın 'Asistan'. 
Asla İngilizce cevap verme. Sadece Türkçe konuş. 
Kısa, net ve samimi ol. Kullanıcının verdiği talimatlara harfiyen uy.
```

Then appends the tenant's custom `system_prompt`:

```python
complete_prompt = TURKISH_BASE_PROMPT + "\n\n" + tenant.system_prompt
```

### Service Flow

```
1. Initialize AIService(tenant_id, db)
   ↓
2. Fetch tenant from database
   ↓
3. Decrypt OpenAI API key
   ↓
4. Build complete system prompt (base + custom)
   ↓
5. Initialize OpenAI client with tenant's key
   ↓
6. Ready to handle chat requests
```

---

## 📚 AIService Class

### Initialization

```python
from app.core.ai_service import AIService, create_ai_service
from app.core.database import SessionLocal

# Method 1: Direct instantiation
db = SessionLocal()
ai_service = AIService(tenant_id=1, db=db)

# Method 2: Factory function (recommended)
ai_service = create_ai_service(tenant_id=1, db=db)
```

### Main Methods

#### 1. `chat_completion()`

Generate a standard chat completion.

```python
response = ai_service.chat_completion(
    user_message="Merhaba! Randevu almak istiyorum.",
    conversation_history=[
        {"role": "user", "content": "Önceki mesaj"},
        {"role": "assistant", "content": "Önceki cevap"}
    ],
    model="gpt-4o",
    temperature=0.7,
    max_tokens=500
)

print(response)  # String response from assistant
```

**Parameters:**
- `user_message` (str, required): User's message
- `conversation_history` (List[Dict], optional): Previous messages
- `model` (str, default="gpt-4o"): OpenAI model
- `temperature` (float, default=0.7): Randomness (0.0-2.0)
- `max_tokens` (int, optional): Max response length

**Returns:**
- `str`: Assistant's response

**Raises:**
- `AIServiceError`: If API call fails

#### 2. `chat_completion_stream()`

Generate a streaming chat completion (yields chunks).

```python
for chunk in ai_service.chat_completion_stream(
    user_message="Klinik hizmetleri nelerdir?",
    model="gpt-4o-mini",
    temperature=0.8
):
    print(chunk, end='', flush=True)
```

**Parameters:** Same as `chat_completion()`

**Yields:**
- `str`: Chunks of assistant's response

#### 3. `validate_api_key()`

Test if tenant's API key is valid.

```python
is_valid = ai_service.validate_api_key()
if is_valid:
    print("✅ API key is working")
else:
    print("❌ API key is invalid")
```

**Returns:**
- `bool`: True if valid, False otherwise

#### 4. `get_available_models()`

Get list of available OpenAI models.

```python
models = ai_service.get_available_models()
print(models)
# ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']
```

**Returns:**
- `List[str]`: Model names

#### 5. `get_tenant_info()`

Get tenant configuration details.

```python
info = ai_service.get_tenant_info()
print(info)
# {
#     "tenant_id": 1,
#     "business_name": "Demo Diş Kliniği",
#     "username": "demo",
#     "has_api_key": True,
#     "system_prompt_length": 450,
#     "created_at": "2026-02-07T10:00:00"
# }
```

**Returns:**
- `Dict`: Tenant information

---

## 🔌 API Endpoints

### 1. POST `/api/chat`

Standard chat completion.

**Request Body:**
```json
{
  "tenant_id": 1,
  "user_message": "Merhaba! Saat kaçta açıksınız?",
  "conversation_history": [
    {
      "role": "user",
      "content": "Önceki mesaj"
    },
    {
      "role": "assistant",
      "content": "Önceki cevap"
    }
  ],
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 500
}
```

**Response:**
```json
{
  "tenant_id": 1,
  "business_name": "Demo Diş Kliniği",
  "user_message": "Merhaba! Saat kaçta açıksınız?",
  "assistant_message": "Merhaba! Kliniğimiz Pazartesi-Cuma 09:00-18:00, Cumartesi 09:00-14:00 arası açıktır. Pazar günleri kapalıyız.",
  "model": "gpt-4o-mini",
  "success": true
}
```

### 2. POST `/api/chat/stream`

Streaming chat completion.

**Request Body:** Same as `/api/chat`

**Response:** 
- Content-Type: `text/plain`
- Headers: `X-Tenant-ID`, `X-Model`
- Body: Streaming text chunks

### 3. GET `/api/tenant/{tenant_id}/models`

Get available models for tenant.

**Response:**
```json
{
  "tenant_id": 1,
  "business_name": "Demo Diş Kliniği",
  "available_models": [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo"
  ]
}
```

### 4. GET `/api/tenant/{tenant_id}/validate`

Validate tenant's API key.

**Response:**
```json
{
  "tenant_id": 1,
  "business_name": "Demo Diş Kliniği",
  "api_key_valid": true,
  "message": "API key is valid and working"
}
```

### 5. GET `/api/tenant/{tenant_id}/info`

Get tenant AI configuration.

**Response:**
```json
{
  "success": true,
  "tenant_info": {
    "tenant_id": 1,
    "business_name": "Demo Diş Kliniği",
    "username": "demo",
    "has_api_key": true,
    "system_prompt_length": 450,
    "created_at": "2026-02-07T10:00:00"
  },
  "system_prompt_preview": "Sen yardımsever bir Türk asistansın..."
}
```

---

## 🧪 Testing

### Run Test Suite

```bash
python test_ai_service.py
```

**Tests Included:**
1. ✅ Get tenant AI info
2. ✅ Validate API key
3. ✅ Get available models
4. ✅ Simple chat completion
5. ✅ Chat with conversation history
6. ✅ Streaming chat completion
7. ✅ Different temperature settings
8. ✅ Error handling

### Manual Testing with cURL

#### Chat Completion
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "user_message": "Merhaba! Randevu almak istiyorum.",
    "model": "gpt-4o-mini",
    "temperature": 0.7
  }'
```

#### Streaming Chat
```bash
curl -X POST "http://localhost:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": 1,
    "user_message": "Klinik hizmetlerinizi anlatır mısınız?",
    "model": "gpt-4o-mini"
  }'
```

#### Validate API Key
```bash
curl "http://localhost:8000/api/tenant/1/validate"
```

---

## 💡 Usage Examples

### Example 1: Simple Chat

```python
from app.core.ai_service import create_ai_service
from app.core.database import SessionLocal

db = SessionLocal()
ai_service = create_ai_service(tenant_id=1, db=db)

response = ai_service.chat_completion(
    user_message="Merhaba! Nasılsınız?"
)

print(response)
# "Merhaba! Ben iyiyim, teşekkür ederim. Size nasıl yardımcı olabilirim?"
```

### Example 2: Multi-turn Conversation

```python
conversation = []

# Turn 1
user_msg_1 = "Randevu almak istiyorum."
response_1 = ai_service.chat_completion(
    user_message=user_msg_1,
    conversation_history=conversation
)

conversation.append({"role": "user", "content": user_msg_1})
conversation.append({"role": "assistant", "content": response_1})

# Turn 2
user_msg_2 = "Yarın için uygun mu?"
response_2 = ai_service.chat_completion(
    user_message=user_msg_2,
    conversation_history=conversation
)

print(response_2)
```

### Example 3: Streaming Response

```python
print("Assistant: ", end='')

for chunk in ai_service.chat_completion_stream(
    user_message="Tedavi hizmetlerinizi detaylı anlatır mısınız?"
):
    print(chunk, end='', flush=True)

print()  # New line at end
```

### Example 4: Different Models

```python
# Fast and cheap
response = ai_service.chat_completion(
    user_message="Hızlı cevap",
    model="gpt-3.5-turbo"
)

# Balanced (default)
response = ai_service.chat_completion(
    user_message="Normal cevap",
    model="gpt-4o-mini"
)

# Most capable
response = ai_service.chat_completion(
    user_message="Detaylı analiz",
    model="gpt-4o"
)
```

### Example 5: Temperature Control

```python
# Very deterministic (consistent responses)
response = ai_service.chat_completion(
    user_message="Çalışma saatleri?",
    temperature=0.0
)

# Balanced
response = ai_service.chat_completion(
    user_message="Genel bilgi",
    temperature=0.7
)

# Creative
response = ai_service.chat_completion(
    user_message="Yaratıcı öneri",
    temperature=1.5
)
```

---

## 🔐 Security

### API Key Protection

1. **Encrypted Storage**
   - API keys stored with Fernet encryption
   - Automatically decrypted only when needed
   - Never logged or exposed

2. **Tenant Isolation**
   - Each tenant has their own API key
   - No shared keys between tenants
   - Separate OpenAI client instances

3. **Error Handling**
   - API keys never included in error messages
   - Secure logging (no sensitive data)
   - Graceful failures

---

## ⚙️ Configuration

### Environment Variables

```bash
# .env file
OPENAI_DEFAULT_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
```

### Model Selection Guide

| Model | Speed | Cost | Use Case |
|-------|-------|------|----------|
| gpt-3.5-turbo | ⚡⚡⚡ | 💰 | Quick responses |
| gpt-4o-mini | ⚡⚡ | 💰💰 | Balanced (default) |
| gpt-4o | ⚡ | 💰💰💰 | Complex tasks |
| gpt-4-turbo | ⚡ | 💰💰💰💰 | Advanced reasoning |

### Temperature Guide

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0.0 - 0.3 | Very deterministic | FAQ, factual info |
| 0.4 - 0.7 | Balanced | General chat (default) |
| 0.8 - 1.2 | Creative | Suggestions, ideas |
| 1.3 - 2.0 | Very creative | Storytelling |

---

## 🐛 Error Handling

### Common Errors

#### 1. Tenant Not Found
```python
AIServiceError: Tenant with ID 999 not found
```
**Solution:** Verify tenant exists in database

#### 2. API Key Not Configured
```python
AIServiceError: OpenAI API key not configured for tenant: Demo Kliniği
```
**Solution:** Set API key via admin panel

#### 3. API Key Invalid
```python
OpenAI API error: Incorrect API key provided
```
**Solution:** Update with valid OpenAI API key

#### 4. Rate Limit
```python
OpenAI API error: Rate limit exceeded
```
**Solution:** Wait or upgrade OpenAI plan

#### 5. Token Limit
```python
OpenAI API error: Maximum context length exceeded
```
**Solution:** Reduce conversation_history or max_tokens

---

## 📊 Logging

### Log Levels

```python
import logging

# Set log level
logging.basicConfig(level=logging.INFO)

# Available levels:
# - DEBUG: Detailed diagnostic info
# - INFO: General informational messages
# - WARNING: Warning messages
# - ERROR: Error messages
```

### Log Examples

```
INFO: Tenant loaded: Demo Diş Kliniği (ID: 1)
INFO: API key decrypted successfully for tenant: 1
INFO: OpenAI client initialized for tenant: 1
INFO: Sending chat completion request for tenant 1
DEBUG: Model: gpt-4o-mini, Temperature: 0.7, Messages: 3
INFO: Chat completion successful for tenant 1
```

---

## 🚀 Performance Tips

1. **Use gpt-4o-mini** for most tasks (faster + cheaper)
2. **Set max_tokens** to limit response length
3. **Reuse AIService** instance for multiple requests
4. **Use streaming** for long responses (better UX)
5. **Cache** common responses (e.g., FAQ)

---

## 📖 API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎓 Best Practices

### 1. System Prompt Design

✅ **Good:**
```
Sen Demo Diş Kliniği'nin sanal resepsiyonistisin.

Çalışma Saatleri: Pazartesi-Cuma 09:00-18:00
Muayene Ücreti: 500 TL
Adres: Kadıköy, İstanbul

Randevu al, bilgi ver, yardımcı ol.
```

❌ **Bad:**
```
You are an AI assistant. Help users with appointments.
```

### 2. Conversation History

✅ **Include context** for multi-turn conversations
❌ **Don't send** entire conversation (limit to last 10 messages)

### 3. Error Handling

✅ **Always** wrap AI calls in try-except
✅ **Provide** user-friendly error messages
✅ **Log** errors for debugging

---

## 🔮 Future Enhancements

- [ ] Function calling support
- [ ] Vision capabilities (image input)
- [ ] Audio transcription integration
- [ ] Response caching
- [ ] Usage analytics
- [ ] Rate limiting per tenant
- [ ] Custom model fine-tuning

---

🇹🇷 **Tamamen Türkçe - Automatic Turkish Language Enforcement**

✅ **AI Service: COMPLETE & PRODUCTION-READY**
