# 🤖 AI-Powered Helpdesk Automation

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37+-red.svg)
![Android](https://img.shields.io/badge/Android-API%2024+-brightgreen.svg)
![Salesforce](https://img.shields.io/badge/Salesforce-Integration-blue.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-orange.svg)

**An intelligent customer support system that uses Google Gemini AI to classify queries, predict priority, generate responses, and integrate with Salesforce CRM.**

[📋 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 📋 Features

### 🤖 AI-Powered Intelligence
- **Smart Query Classification**: Automatically categorizes customer queries into Billing, Technical Issue, Product Inquiry, Feedback, or General Inquiry
- **Intelligent Priority Prediction**: Determines Low, Medium, or High priority based on urgency analysis
- **Automated Response Generation**: Creates contextual, helpful responses using Google Gemini AI
- **Confidence Scoring**: Provides confidence levels for all AI predictions

### 🔗 Enterprise Integration
- **Salesforce CRM Integration**: Seamlessly creates records in Case object in Salesforce Developer Org with custom fields
- **Custom Field Mapping**: Stores AI predictions, responses, and metadata in Salesforce
- **Escalation Workflow**: Option to escalate cases to human agents with proper status tracking resulting in making the satus of the Case as `open`
- **Real-time Synchronization**: Instant case creation and status updates
- **Web Interface**: Modern Streamlit web application for easy access
- **REST API**: FastAPI-based backend with comprehensive endpoints
- **Android Mobile App**: Native Kotlin app with Material Design 3


### System Flow:
1. **Input Processing**: Customer submits query via Web/Android
2. **AI Analysis**: Google Gemini analyzes and classifies the query
3. **Response Generation**: AI generates contextual response
4. **CRM Integration**: Case created in Salesforce with all metadata
5. **Status Updates**: Real-time feedback to user interface

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** - Backend runtime
- **Android Studio** (for Android app development)
- **Salesforce Developer Org** account
- **Google Gemini API** key
- **Git** for version control

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/Deba951/ai-helpdesk-automation.git
cd ai-helpdesk-automation

# Create virtual environment
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Salesforce Setup

#### Create Developer Org
1. Visit [Salesforce Developer](https://developer.salesforce.com/signup)
2. Create free Developer Org account
3. Verify email and complete setup

#### Configure Custom Fields
Navigate to **Setup → Object Manager → Case → Fields & Relationships** and create:

| Field Label | API Name | Type | Length |
|-------------|----------|------|--------|
| AI Predicted Category | `AI_Predicted_Category__c` | Text | 50 |
| AI Predicted Priority | `AI_Predicted_Priority__c` | Text | 20 |
| AI Response | `AI_Response__c` | Long Text Area | 32,768 |
| Escalated | `Escalated__c` | Checkbox | Unchecked |

#### Get Security Token
1. Click profile picture → **Settings**
2. **Reset My Security Token** (check email)
3. Token is 25 characters long

### 3. Configuration

Create `.env` file in project root:

```env
# Salesforce Configuration
SALESFORCE_USERNAME=your_username@domain.com
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_25_char_token
SALESFORCE_DOMAIN=login  # Use 'test' for sandbox, 'login' for production or developer org

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the System

#### Backend API
```bash
python api.py
# Server starts on http://localhost:8000
```

#### Streamlit Web Interface
```bash
streamlit run streamlit_app.py
# Opens at http://localhost:8501
```

#### Android App
1. Open `androidApp/` in Android Studio
2. Update API URL in `MainActivity.kt`:
   ```kotlin
   private val API_URL = "http://YOUR_IP:8000"
   ```
3. Build and run on emulator/device

---

## 📖 Documentation

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict` | AI prediction only |
| `POST` | `/create_case` | Full pipeline with Salesforce |

#### Example API Usage

```bash
# AI Prediction Only
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "query": "Billing question about invoice"
  }'

# Full Case Creation
curl -X POST "http://localhost:8000/create_case" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "query": "Billing question about invoice",
    "escalated": false
  }'
```

### Response Format

```json
{
  "customer_name": "John Doe",
  "query": "Billing question about invoice",
  "category": "Billing",
  "priority": "Medium",
  "response": "Thank you for your inquiry...",
  "confidence": 0.95,
  "salesforce_case_id": "500dL000024IbqbQAC",
  "salesforce_status": "Closed",
  "escalated": false
}
```

### Categories & Priorities

**Query Categories:**
- 📄 **Billing** - Payment and invoice related
- 🔧 **Technical Issue** - Technical problems and bugs
- 🛍️ **Product Inquiry** - Product information requests
- 💬 **Feedback** - Customer feedback and suggestions
- ❓ **General Inquiry** - General questions

**Priority Levels:**
- 🟢 **Low** - Non-urgent requests
- 🟡 **Medium** - Standard priority
- 🔴 **High** - Urgent issues requiring immediate attention

---

## 📁 Project Structure

```
ai-helpdesk-automation/
├── 📄 ai_engine.py              # Google Gemini AI integration
├── 📄 api.py                    # FastAPI backend server
├── 📄 streamlit_app.py          # Web interface
├── 📄 salesforce_integration.py # Salesforce CRM integration
├── 📄 test_salesforce.py        # Connection testing utilities
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment configuration
├── 📱 androidApp/               # Android application
│   ├── 📱 app/src/main/
│   │   ├── 📄 AndroidManifest.xml
│   │   ├── 📱 java/com/example/aihelpdesk/
│   │   │   └── 📄 MainActivity.kt
│   │   └── 📱 res/               # UI resources
│   └── 📄 build.gradle.kts      # Android dependencies
└── 📊 data/                     # Sample datasets
```

---

## 🧪 Testing

### Test Salesforce Connection
```bash
python test_salesforce.py
```

Expected output:
```
✅ Successfully connected to Salesforce!
📊 Found X cases in your org
✅ Test case created successfully!
🗑️ Test case cleaned up
🎉 All tests passed!
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Test", "query": "Test query"}'
```

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for intelligent customer support automation

</div>
