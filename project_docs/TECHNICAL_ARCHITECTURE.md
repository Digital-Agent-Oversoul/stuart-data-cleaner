# Stuart Data Cleaning System - Technical Architecture

## 🏗️ **System Overview**

### **Architecture Pattern**
The Stuart Data Cleaning System follows a **modular, multi-tier architecture** with complete process independence and shared core services.

### **Core Principles**
- **Process Isolation**: Survey and Contact Export processes operate independently
- **Shared Core Engine**: Common data processing logic for consistency
- **Multi-tier Fallback**: OpenAI → Ollama → Rule-based processing
- **Interactive Learning**: Human-in-the-loop system for edge cases

## 🔧 **System Components**

### **1. Core Data Processing Engine**
```
┌─────────────────────────────────────────────────────────────┐
│                    Core Processing Engine                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Data Loader   │  │  Data Cleaner   │  │ Data Output │ │
│  │                 │  │                 │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Name Parser    │  │  Email Cleaner  │  │ Phone      │ │
│  │  (LLM + Rules) │  │                 │  │ Formatter   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **2. Multi-Tier LLM System**
```
┌─────────────────────────────────────────────────────────────┐
│                    LLM Processing Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   OpenAI API    │  │   Ollama API    │  │ Rule-Based  │ │
│  │  (Primary)      │  │  (Fallback)     │  │ (Emergency) │ │
│  │  gpt-4o-mini    │  │  qwen2.5:7b     │  │ Processing  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Budget Monitor │  │  Cost Tracker   │  │ Fallback    │ │
│  │                 │  │                 │  │ Controller  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **3. Interactive Learning Framework**
```
┌─────────────────────────────────────────────────────────────┐
│                    Interactive Learning System              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Uncertainty     │  │ Human-in-the-   │  │ Pattern     │ │
│  │ Detector        │  │ Loop Prompts     │  │ Learner     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ Confidence      │  │ Decision        │  │ Knowledge   │ │
│  │ Scorer          │  │ Memory          │  │ Base        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📊 **Data Flow Architecture**

### **Input Processing Flow**
```
Raw Excel File → Data Loader → Validation → Core Engine → Process Router
                                                      ↓
                                    ┌─────────────────┬─────────────────┐
                                    │                 │                 │
                                    ▼                 ▼                 ▼
                              Survey Process    Contact Export    Quality Monitor
                                    │                 │                 │
                                    ▼                 ▼                 ▼
                              Location-Based    Aggregated File    Validation
                              Output Files      with Removed      Reports
                                               Items Sheet
```

### **LLM Processing Flow**
```
Name Data → Uncertainty Check → Confidence Score → Decision Point
     ↓              ↓                ↓              ↓
  < 0.7         < 0.5           < 0.3         > 0.7
     ↓              ↓                ↓              ↓
  OpenAI        Ollama         Rule-Based    Use LLM Result
     ↓              ↓                ↓
  Success?      Success?        Always
     ↓              ↓                ↓
     Yes           Yes             Yes
     ↓              ↓                ↓
  Use Result    Use Result      Use Result
```

## 🔐 **Configuration Management**

### **Environment Variables**
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.1

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct-q4_K_M
OLLAMA_FALLBACK_ENABLED=true

# Budget Configuration
OPENAI_MONTHLY_BUDGET=10.00
OPENAI_ALERT_THRESHOLD=0.8
```

### **JSON Configuration Files**
```json
{
  "llm": {
    "openai": {
      "model": "gpt-4o-mini",
      "max_tokens": 150,
      "temperature": 0.1
    },
    "ollama": {
      "base_url": "http://localhost:11434",
      "model": "qwen2.5:7b-instruct-q4_K_M"
    }
  },
  "processing": {
    "batch_size": 500,
    "max_rows_for_llm": 1000,
    "confidence_thresholds": {
      "high": 0.7,
      "medium": 0.5,
      "low": 0.3
    }
  },
  "output": {
    "survey": {
      "base_dir": "Broadly Cleaned",
      "location_segments": ["Dublin", "Milpitas"]
    },
    "contact_export": {
      "base_dir": "Email Contact Export",
      "include_removed_items": true
    }
  }
}
```

## 🏛️ **Process Architecture**

### **Survey Process (Independent)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Survey Process                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Input Handler  │  │  Core Engine    │  │ Location    │ │
│  │                 │  │  (Shared)       │  │ Segmenter   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Dublin Output  │  │ Milpitas Output │  │ Quality     │ │
│  │  Generator      │  │ Generator       │  │ Reporter    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Contact Export Process (Independent)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Contact Export Process                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Input Handler  │  │  Core Engine    │  │ Contact     │ │
│  │                 │  │  (Shared)       │  │ Validator   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Main Output    │  │ Removed Items   │  │ Quality     │ │
│  │  Generator      │  │ Sheet Generator │  │ Reporter    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 **Interactive Learning Architecture**

### **Learning Flow**
```
Edge Case Detected → Uncertainty Analysis → User Prompt → Decision Capture
       ↓                    ↓                ↓              ↓
   Confidence < 0.7    Pattern Match?    User Input    Store Decision
       ↓                    ↓                ↓              ↓
   Prompt User         Similar Case?     Validate      Update Patterns
       ↓                    ↓                ↓              ↓
   Wait for Input      Apply Learning    Confirm       Improve Prompts
       ↓                    ↓                ↓              ↓
   Process Decision    Update Confidence  Continue      Next Case
```

### **Pattern Learning Components**
```
┌─────────────────────────────────────────────────────────────┐
│                    Pattern Learning System                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Case           │  │  Decision       │  │ Pattern     │ │
│  │  Analyzer       │  │  Extractor      │  │ Matcher     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Confidence     │  │  Prompt         │  │ Knowledge   │ │
│  │  Updater        │  │  Optimizer      │  │ Base        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🛡️ **Error Handling & Resilience**

### **Error Handling Strategy**
```
Error Detected → Error Classification → Recovery Action → Fallback System
      ↓                ↓                ↓              ↓
   LLM Failure    API Error?        Retry Logic    Switch to Ollama
      ↓                ↓                ↓              ↓
   Network Issue   Rate Limit?      Wait & Retry   Switch to Rules
      ↓                ↓                ↓              ↓
   Budget Limit    Cost Exceeded?   Alert User     Stop Processing
      ↓                ↓                ↓              ↓
   Data Error      Validation?      Log Error      Skip Record
```

### **Fallback Mechanisms**
1. **Primary**: OpenAI API (gpt-4o-mini)
2. **Secondary**: Ollama local (qwen2.5:7b)
3. **Tertiary**: Rule-based processing
4. **Emergency**: User manual intervention

## 📈 **Performance & Scalability**

### **Performance Targets**
- **Small Datasets** (<1K rows): <5 minutes processing
- **Medium Datasets** (1K-10K rows): <15 minutes processing
- **Large Datasets** (>10K rows): <30 minutes processing
- **LLM Response Time**: <10 seconds per name parsing request

### **Scalability Considerations**
- **Batch Processing**: Configurable batch sizes for large files
- **Memory Management**: Efficient data handling for large datasets
- **Parallel Processing**: Independent process execution
- **Resource Monitoring**: Real-time performance tracking

## 🔒 **Security & Privacy**

### **Data Security**
- **Local Processing**: Data processed locally, not sent to external services
- **API Key Management**: Secure storage and rotation of OpenAI keys
- **Audit Logging**: Complete tracking of all processing decisions
- **Data Validation**: Input validation and sanitization

### **Privacy Considerations**
- **Customer Data**: Sensitive information handled securely
- **Learning Data**: User decisions stored locally
- **No External Sharing**: Data not shared with third parties
- **Compliance**: Maintain data integrity and audit trails

## 🚀 **Deployment Architecture**

### **Development Environment**
```
┌─────────────────────────────────────────────────────────────┐
│                    Development Setup                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Local Python   │  │  Ollama Local   │  │  OpenAI     │ │
│  │  Environment    │  │  Installation   │  │  API Access │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  CLI Interface  │  │  Test Datasets  │  │  Local      │ │
│  │  for Testing    │  │  for Validation │  │  Output     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Production Environment (Future)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Production Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Web Interface  │  │  REST API       │  │  Scheduled  │ │
│  │  (Archon-style) │  │  Endpoints      │  │  Processing │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Email          │  │  Workflow       │  │  Monitoring │ │
│  │  Integration    │  │  Automation     │  │  & Alerts   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-08  
**Next Review**: After Phase 1 completion  
**Document Owner**: Stuart Project Team
